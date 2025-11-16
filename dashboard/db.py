from sqlalchemy import create_engine, text
import pandas as pd
import os
import re
from datetime import datetime, timedelta
from typing import Optional

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")

if not (DB_USER and DB_PASSWORD and DB_HOST and DB_NAME):
    engine = None
else:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", pool_pre_ping=True)


def list_public_tables():
    if engine is None:
        return []
    with engine.connect() as conn:
        res = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables"))
        return [r[0] for r in res.fetchall()]


def find_table_like(keywords):
    tables = list_public_tables()
    for t in tables:
        name = t.lower()
        if all(k.lower() in name for k in keywords):
            return t
    return None


_MEM_CACHE = {}


def clear_cache(table_name: Optional[str] = None):
    if table_name is None:
        _MEM_CACHE.clear()
    else:
        keys = [k for k in _MEM_CACHE.keys() if k[0] == table_name]
        for k in keys:
            _MEM_CACHE.pop(k, None)


def _is_time_like(col: str) -> bool:
    return bool(re.search(r"time|date|timetag|processedat|processed_at|observed", col))


def read_table(table_name: str, limit: Optional[int] = None, use_cache: bool = True, ttl_seconds: Optional[int] = None, force_refresh: bool = False) -> pd.DataFrame:
    """
    Read data from a table

    :param table_name:
    :param limit:
    :param ttl_seconds:
    :param force_refresh:
    :return:
    """
    if table_name is None:
        return pd.DataFrame()

    key = (table_name, int(limit) if limit is not None else None)

    # try memory cache
    if use_cache and not force_refresh:
        entry = _MEM_CACHE.get(key)
        if entry is not None:
            ts = entry.get('ts')
            if ttl_seconds is None or (datetime.now() - ts) <= timedelta(seconds=ttl_seconds):
                # return cached copy to prevent accidental mutation
                return entry['df'].copy()

    if engine is None:
        raise RuntimeError("DB engine not configured (set DB_USER/DB_PASSWORD/DB_HOST/DB_NAME)")

    q = f'SELECT * FROM "{table_name}"'
    if limit:
        q += f" LIMIT {limit}"
    df = pd.read_sql(text(q), con=engine)
    # normalize column names
    df.columns = [c.lower() for c in df.columns]

    for c in df.columns:
        if _is_time_like(c):
            try:
                df[c] = pd.to_datetime(df[c])
            except Exception:
                pass

    try:
        _MEM_CACHE[key] = {'ts': datetime.now(), 'df': df.copy()}
    except Exception:
        pass

    return df


def pick_time_column(df: pd.DataFrame) -> Optional[str]:
    if df is None or df.empty:
        return None
    candidates = [c for c in df.columns if _is_time_like(c)]
    if not candidates:
        return None
    for c in candidates:
        if "timetag" in c or c == "time" or c.endswith("_at"):
            return c
    return candidates[0]
