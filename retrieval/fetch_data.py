"""Fetch data from NOAA SWPC APIs and package for Dropbox upload."""

import asyncio
import csv
from datetime import datetime
from pathlib import Path
from shutil import make_archive, rmtree
from typing import Optional, Union

import aiohttp

from retrieval.logger import Logger
from retrieval.send2dropbox import send_to_dropbox
from retrieval.url_mapping import NAME2URL

SAVE_DIR = Path(__file__).parent / "data"
RETRY_SLEEP_TIME = 15
MAX_RETRIES = 3
SAVE_DIR.mkdir(parents=True, exist_ok=True)
DROPBOX_DIR = "/inzynierka"

logger = Logger()


async def retrieve_data(
    session: aiohttp.ClientSession,
    target_name: str,
    url: str,
    target_dir: Union[str, Path] = SAVE_DIR,
) -> Optional[Path]:
    """Retrieve data for a specific URL with per-file retry tolerance.

    Makes up to MAX_RETRIES fresh HTTP requests. On permanent failure,
    returns None so the file is excluded from the final archive rather
    than crashing the entire pipeline.

    Args:
        session: Shared aiohttp session for connection pooling.
        target_name: Logical name of the data source.
        url: Remote JSON endpoint to fetch.
        target_dir: Local directory to save the resulting CSV.

    Returns:
        Path to the saved CSV file on success, or None on failure.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            logger.log(
                f"Retrieving data from {url} "
                f"(attempt {attempt}/{MAX_RETRIES})"
            )
            async with session.get(url) as response:
                if not response.ok:
                    raise aiohttp.ClientResponseError(
                        request_info=response.request_info,
                        history=response.history,
                        status=response.status,
                        message=f"HTTP {response.status}",
                    )

                data = await response.json()

                if not data:
                    raise ValueError(
                        "No data found for the given date range"
                    )

                # Flatten nested dict structures if present
                has_nested = any(
                    isinstance(item, dict) for item in data
                )
                if has_nested:
                    logger.log_warning(
                        f"Data contains nested structures, "
                        f"flattening the data for {target_name}"
                    )
                    data = [
                        {
                            **item,
                            **{
                                k: v
                                for k, v in item.items()
                                if isinstance(v, dict)
                            },
                        }
                        for item in data
                    ]

                # Append the data to a CSV file
                filename = (
                    target_dir
                    / f"{target_name}_{datetime.today().date()}.csv"
                )
                with open(filename, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    # Write the header only if the file is empty
                    if file.tell() == 0:
                        logger.log(
                            f"Writing header for {target_name} "
                            f"to {filename}"
                        )
                        writer.writerow(data[0].keys())
                    for item in data:
                        writer.writerow(item.values())

                logger.log(
                    f"Data retrieved and saved to {filename}"
                )
                return filename

        except Exception as exc:
            logger.log_error(
                f"Error retrieving data from {url}: {exc}. "
                f"Attempt {attempt}/{MAX_RETRIES}"
            )
            if attempt < MAX_RETRIES:
                logger.log(
                    f"Sleeping for {RETRY_SLEEP_TIME} seconds "
                    f"before retrying"
                )
                await asyncio.sleep(RETRY_SLEEP_TIME)

    # All retries exhausted — file will be excluded from archive
    logger.log_error(
        f"Permanently failed to retrieve {target_name} from {url} "
        f"after {MAX_RETRIES} retries. "
        f"This source will be excluded from the archive."
    )
    return None


def compress_data(
    target_name: str,
    target_dir: Union[str, Path] = SAVE_DIR,
    remove_dir: bool = True,
) -> None:
    """Compress the data directory into a zip file.

    Args:
        target_name: Base name for the resulting archive.
        target_dir: Directory whose contents will be archived.
        remove_dir: Whether to remove the source directory after
            compression.
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Compressing data for {target_name}")
    make_archive(
        base_name=str(target_dir.parent / target_name),
        format="zip",
        root_dir=target_dir.parent,
        base_dir=target_dir.name,
    )

    if remove_dir:
        logger.log(f"Removing directory {target_dir}")
        rmtree(target_dir, ignore_errors=False)
        logger.log(f"Directory {target_dir} removed")


async def retrieve_all_data() -> None:
    """Retrieve all data sources; failed files are excluded from archive.

    Uses a shared aiohttp session for connection pooling.
    Individual source failures do not abort the pipeline — only
    successfully fetched files are included in the final zip archive.
    """
    target_dir = SAVE_DIR / f"{datetime.today().date()}"
    names = list(NAME2URL.keys())

    async with aiohttp.ClientSession() as session:
        tasks = [
            retrieve_data(session, name, url, target_dir)
            for name, url in NAME2URL.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

    # Separate successes from failures
    failed_sources = []
    succeeded_sources = []
    for name, result in zip(names, results):
        if isinstance(result, Exception) or result is None:
            failed_sources.append(name)
        else:
            succeeded_sources.append(name)

    # Log summary
    if failed_sources:
        logger.log_warning(
            f"Excluded {len(failed_sources)} source(s) from archive: "
            f"{failed_sources}"
        )

    if not succeeded_sources:
        logger.log_error(
            "All sources failed. No archive will be created."
        )
        # Clean up the empty target directory if it exists
        if target_dir.exists():
            rmtree(target_dir, ignore_errors=True)
        return

    logger.log(
        f"Successfully retrieved {len(succeeded_sources)} "
        f"source(s): {succeeded_sources}"
    )
    logger.log(f"All data retrieved and saved to {target_dir}")

    compress_data(target_dir.name, target_dir)
    logger.log(f"Data compressed to {target_dir}.zip")

    send_to_dropbox(
        target_dir.parent / f"{target_dir.name}.zip",
        f"{DROPBOX_DIR}/{target_dir.name}.zip",
        logger,
    )


if __name__ == "__main__":
    asyncio.run(retrieve_all_data())
