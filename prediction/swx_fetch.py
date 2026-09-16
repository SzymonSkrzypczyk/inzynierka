#!/usr/bin/env python3
"""
swx_fetch.py — LASP Space Weather Portal CLI data downloader
=============================================================
Fetches space-weather time-series from the LASP LaTiS API
(https://lasp.colorado.edu/space-weather-portal/about/latis)
and writes each parameter to its own CSV file.

Usage
-----
  python swx_fetch.py --start "2024-05-10" --end "2024-05-12"
  python swx_fetch.py --start "2024-05-10T00:00:00" --end "2024-05-10T06:00:00"
  python swx_fetch.py --start "May 10, 2024" --end "May 12, 2024" --params kp bz
  python swx_fetch.py --start "2024-05-10" --end "2024-05-12" --outdir ./data

Optimised for efficiency using:
- Async I/O (asyncio + httpx)
- Connection pooling (reusing TCP/SSL connections)
- Gzip compression (automatic via httpx)
- Parallel chunking (downloading 14-day segments concurrently)
"""

import argparse
import asyncio
import csv
import io
import sys
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from tqdm.asyncio import tqdm

# ---------------------------------------------------------------------------
# LaTiS API configuration
# ---------------------------------------------------------------------------

BASE_URL = "https://lasp.colorado.edu/space-weather-portal/latis/dap"

# Many high-res datasets on LaTiS have a limit on the time range per query.
# 14 days is a common safe limit for 1-minute cadence data.
MAX_DAYS_PER_REQUEST = 14

# Limit concurrent requests to prevent server throttling
MAX_CONCURRENT_REQUESTS = 15

# Each entry describes how to query a single parameter:
#   dataset   – LaTiS dataset name
#   variable  – column to pull from that dataset (plus 'time')
#   label     – human-readable name printed in progress messages
PARAM_MAP = {
    "kp": {
        "dataset": "potsdam_kp",
        "variable": "kp",
        "label": "Planetary K-index (Kp)",
    },
    "bx": {
        "dataset": "ace_mag_1m",
        "variable": "Bx",
        "label": "IMF Bx (nT)",
    },
    "by": {
        "dataset": "ace_mag_1m",
        "variable": "By",
        "label": "IMF By (nT)",
    },
    "bz": {
        "dataset": "ace_mag_1m",
        "variable": "Bz",
        "label": "IMF Bz (nT)",
    },
    "speed": {
        "dataset": "ace_swepam_1m",
        "variable": "speed",
        "label": "Solar Wind Speed (km/s)",
    },
}

DEFAULT_PARAMS = list(PARAM_MAP.keys())

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_DATETIME_FORMATS = [
    "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M", "%Y-%m-%d", "%Y/%m/%d %H:%M:%S",
    "%Y/%m/%d %H:%M", "%Y/%m/%d", "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y %H:%M", "%d-%m-%Y", "%B %d %Y %H:%M:%S",
    "%B %d %Y %H:%M", "%B %d %Y", "%b %d %Y %H:%M:%S",
    "%b %d %Y %H:%M", "%b %d %Y", "%B %d, %Y %H:%M:%S",
    "%B %d, %Y %H:%M", "%B %d, %Y", "%b %d, %Y %H:%M:%S",
    "%b %d, %Y %H:%M", "%b %d, %Y", "%d %B %Y", "%d %b %Y",
]


def parse_datetime(text: str) -> datetime:
    text = text.strip()
    for fmt in _DATETIME_FORMATS:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse '{text}' as a date/time.")


def fmt_latis(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def fmt_filename(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H%M%S")


def convert_latis_time(val_str: str, units: str) -> str:
    val_str = val_str.strip()
    if not val_str or ("-" in val_str and ":" in val_str):
        return val_str

    if "yyyy MM dd HHmm" in units:
        try:
            dt = datetime.strptime(val_str, "%Y %m %d %H%M").replace(tzinfo=timezone.utc)
            return dt.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return val_str

    try:
        val = float(val_str)
    except ValueError:
        return val_str

    if "milliseconds since 1970" in units:
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(milliseconds=val)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")
    
    if "days since 1932-01-01" in units:
        dt = datetime(1932, 1, 1, tzinfo=timezone.utc) + timedelta(days=val)
        return dt.strftime("%Y-%m-%dT%H:%M:%S")

    return val_str


# ---------------------------------------------------------------------------
# Core Async Fetchers
# ---------------------------------------------------------------------------

async def fetch_chunk(
    client: httpx.AsyncClient, 
    url: str, 
    variable: str, 
    sem: asyncio.Semaphore,
    desc: str
) -> list[dict]:
    """Fetch a single CSV chunk from LaTiS with concurrency control."""
    async with sem:
        try:
            resp = await client.get(url, timeout=120)
            resp.raise_for_status()
            raw = resp.text
        except httpx.HTTPStatusError as exc:
            raise RuntimeError(f"HTTP {exc.response.status_code} for {url}") from exc
        except Exception as exc:
            raise RuntimeError(f"Network error for {url}: {exc}") from exc

    # Parse CSV
    lines = raw.strip().splitlines()
    data_lines = [l for l in lines if not l.startswith("#")]
    if not data_lines:
        return []

    reader = csv.DictReader(io.StringIO("\n".join(data_lines)))
    time_col, var_col = None, None
    if reader.fieldnames:
        for col in reader.fieldnames:
            c_low = col.lower()
            if "time" in c_low: time_col = col
            elif variable.lower() in c_low: var_col = col
    
    if not time_col and reader.fieldnames: time_col = reader.fieldnames[0]
    if not var_col and reader.fieldnames and len(reader.fieldnames) > 1: var_col = reader.fieldnames[1]

    rows = []
    for row in reader:
        time_val = row.get(time_col, "").strip() if time_col else ""
        if time_col:
            time_val = convert_latis_time(time_val, time_col)
        rows.append({
            "time": time_val,
            variable: row.get(var_col, "").strip() if var_col else ""
        })
    return rows


async def fetch_parameter(
    client: httpx.AsyncClient,
    param: str,
    start: datetime,
    end: datetime,
    outdir: Path,
    file_start: str,
    file_end: str,
    sem: asyncio.Semaphore,
) -> bool:
    """Manage chunks for one parameter, then write the CSV."""
    cfg = PARAM_MAP[param]
    dataset = cfg["dataset"]
    variable = cfg["variable"]
    label = cfg["label"]

    # Create chunks
    tasks = []
    curr = start
    while curr < end:
        next_chunk = min(curr + timedelta(days=MAX_DAYS_PER_REQUEST), end)
        
        # Build URL
        q = f"time,{variable}&time>={urllib.parse.quote(fmt_latis(curr))}&time<={urllib.parse.quote(fmt_latis(next_chunk))}"
        url = f"{BASE_URL}/{dataset}.csv?{q}"
        
        tasks.append(fetch_chunk(client, url, variable, sem, f"{param.upper()} {curr.date()}"))
        curr = next_chunk

    # Run chunks concurrently
    chunk_results = await tqdm.gather(*tasks, desc=f"Fetching {param.upper():<5}", leave=False)
    
    all_rows = [row for chunk in chunk_results for row in chunk]
    if not all_rows:
        print(f"  [!] No data for {param.upper()}")
        return False

    # Deduplicate and Sort
    seen = set()
    unique = []
    for r in sorted(all_rows, key=lambda x: x["time"]):
        if r["time"] not in seen:
            unique.append(r)
            seen.add(r["time"])

    # Write
    actual_var = [k for k in unique[0].keys() if k != "time"][0]
    outfile = outdir / f"{param}_{file_start}_{file_end}.csv"
    with outfile.open("w", newline="", encoding="utf-8") as f:
        f.write(f"# Parameter: {label}\n# Source: LaTiS (Optimised Fetch)\n")
        writer = csv.DictWriter(f, fieldnames=["time", actual_var])
        writer.writeheader()
        writer.writerows(unique)
    
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def run_all(args):
    start_dt = parse_datetime(args.start)
    end_dt = parse_datetime(args.end)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    file_start, file_end = fmt_filename(start_dt), fmt_filename(end_dt)

    print("=" * 60)
    print(f"  LASP LaTiS Data fetching tool")
    print(f"  Range  : {fmt_latis(start_dt)} to {fmt_latis(end_dt)}")
    print(f"  Params : {', '.join(args.params)}")
    print("=" * 60)

    sem = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    
    async with httpx.AsyncClient(http2=True, follow_redirects=True) as client:
        tasks = [
            fetch_parameter(client, p, start_dt, end_dt, outdir, file_start, file_end, sem)
            for p in args.params
        ]
        results = await asyncio.gather(*tasks)

    successes = sum(1 for r in results if r)
    print(f"\nCompleted. {successes}/{len(args.params)} parameters saved to '{outdir}'.")


def main():
    parser = argparse.ArgumentParser(description="High-efficiency Space Weather Data Fetcher")
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--params", nargs="+", choices=list(PARAM_MAP.keys()), default=DEFAULT_PARAMS)
    parser.add_argument("--outdir", default="data")
    args = parser.parse_args()

    try:
        asyncio.run(run_all(args))
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
