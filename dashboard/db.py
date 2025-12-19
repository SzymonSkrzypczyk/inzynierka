from sqlalchemy import create_engine, text
import pandas as pd
import os
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, List

logger = logging.getLogger(__name__)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")

if not (DB_USER and DB_PASSWORD and DB_HOST and DB_NAME):
    engine = None
    logger.warning("Database credentials not configured - database operations will fail")
else:
    engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", pool_pre_ping=True)
    logger.info(f"Database engine created for {DB_HOST}:{DB_PORT}/{DB_NAME}")


def list_public_tables():
    """
    List all public tables in the database

    :return:
    """
    if engine is None:
        logger.warning("Cannot list tables - database engine not configured")
        return []
    with engine.connect() as conn:
        res = conn.execute(text("SELECT tablename FROM pg_catalog.pg_tables"))
        tables = [r[0] for r in res.fetchall()]
        logger.info(f"Found {len(tables)} public tables in database")
        return tables


def find_table_like(keywords: List[str]):
    """
    Find a table whose name contains all keywords (case insensitive)

    :param keywords:  list of keywords
    :type keywords: list[str]
    :return:
    """
    logger.debug(f"Searching for table with keywords: {keywords}")
    tables = list_public_tables()
    for t in tables:
        name = t.lower()
        if all(k.lower() in name for k in keywords):
            logger.info(f"Found matching table: {t} for keywords {keywords}")
            return t
    logger.warning(f"No table found matching keywords: {keywords}")
    return None


_MEM_CACHE = {}


def clear_cache(table_name: Optional[str] = None):
    """
    Clear memory cache

    :param table_name: table name to clear, or None to clear all
    :type table_name: Optional[str]
    :return:
    """
    if table_name is None:
        logger.info("Clearing all cache entries")
        _MEM_CACHE.clear()
    else:
        keys = [k for k in _MEM_CACHE.keys() if k[0] == table_name]
        logger.info(f"Clearing cache for table {table_name} ({len(keys)} entries)")
        for k in keys:
            _MEM_CACHE.pop(k, None)


def _is_time_like(col: str) -> bool:
    """
    Check if a column name is time-like

    :param col: column name
    :type col: str
    :return:
    """
    return bool(re.search(r"time|date|timetag|processedat|processed_at|observed", col))


def read_table(table_name: str, limit: Optional[int] = None, use_cache: bool = True, ttl_seconds: Optional[int] = None, force_refresh: bool = False) -> pd.DataFrame:
    """
    Read a table from the database into a pandas DataFrame

    :param table_name:
    :type table_name: str
    :param limit:
    :type limit: Optional[int]
    :param use_cache:
    :type use_cache: bool
    :param ttl_seconds:
    :type ttl_seconds: Optional[int]
    :param force_refresh:
    :type force_refresh: bool
    :return:
    """
    if table_name is None:
        logger.warning("read_table called with None table_name")
        return pd.DataFrame()

    key = (table_name, int(limit) if limit is not None else None)

    # try memory cache
    if use_cache and not force_refresh:
        entry = _MEM_CACHE.get(key)
        if entry is not None:
            ts = entry.get('ts')
            if ttl_seconds is None or (datetime.now() - ts) <= timedelta(seconds=ttl_seconds):
                logger.debug(f"Returning cached data for table {table_name} (limit={limit})")
                # return cached copy to prevent accidental mutation
                return entry['df'].copy()

    if engine is None:
        logger.error("Database engine not configured")
        raise RuntimeError("DB engine not configured (set DB_USER/DB_PASSWORD/DB_HOST/DB_NAME)")

    logger.info(f"Reading table {table_name} from database (limit={limit})")
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
        logger.debug(f"Cached data for table {table_name} (rows={len(df)})")
    except Exception:
        pass

    logger.info(f"Successfully loaded {len(df)} rows from table {table_name}")
    return df


def pick_time_column(df: pd.DataFrame) -> Optional[str]:
    """
    Pick the most likely time column from the DataFrame

    :param df:
    :type df: pd.DataFrame
    :return:
    """
    if df is None or df.empty:
        return None
    candidates = [c for c in df.columns if _is_time_like(c)]
    if not candidates:
        return None
    for c in candidates:
        if "timetag" in c or c == "time" or c.endswith("_at"):
            return c
    return candidates[0]
