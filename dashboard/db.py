from sqlalchemy import create_engine, text
import pandas as pd
import os
import re
import logging
import sys
import threading
import time
import pickle
import zlib
from datetime import datetime, timedelta
from typing import Optional, List, Dict

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
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )
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


MAX_CACHE_SIZE_MB = 100

def _get_cache_key(table_name: str, limit: Optional[int] = None) -> str:
    """Generate semantic cache keys"""
    if limit and limit <= 1000:
        return f"{table_name}_small"
    return f"{table_name}_recent"

def _get_cache_memory_usage() -> int:
    """Calculate total memory usage of cached DataFrames"""
    total_size = 0
    for entry in _MEM_CACHE.values():
        val = entry.get('df')
        if val is not None:
             total_size += val.memory_usage(deep=True).sum()
        else:
             # compressed
             val_c = entry.get('df_compressed')
             if val_c:
                 total_size += len(val_c)
    return total_size

def _manage_cache_size():
    """Remove oldest cache entries when memory limit exceeded"""
    if _get_cache_memory_usage() > MAX_CACHE_SIZE_MB * 1024 * 1024:
        # Remove oldest 50% of entries
        sorted_keys = sorted(_MEM_CACHE.keys(), key=lambda k: _MEM_CACHE[k]['ts'])
        keys_to_remove = sorted_keys[:len(sorted_keys)//2]
        for key in keys_to_remove:
            _MEM_CACHE.pop(key, None)

def _compress_dataframe(df: pd.DataFrame) -> bytes:
    """Compress DataFrame for memory-efficient storage"""
    return zlib.compress(pickle.dumps(df))

def _decompress_dataframe(data: bytes) -> pd.DataFrame:
    """Decompress stored DataFrame"""
    return pickle.loads(zlib.decompress(data))

def _store_in_cache(key: str, df: pd.DataFrame):
    """Store DataFrame in cache with compression for large datasets"""
    _manage_cache_size()  # Ensure space
    if df.memory_usage(deep=True).sum() > 10 * 1024 * 1024:  # > 10MB
        compressed_data = _compress_dataframe(df)
        _MEM_CACHE[key] = {
            'ts': datetime.now(),
            'df_compressed': compressed_data,
            'is_compressed': True
        }
    else:
        _MEM_CACHE[key] = {
            'ts': datetime.now(),
            'df': df.copy(),
            'is_compressed': False
        }

def _get_time_column(table_name: str) -> Optional[str]:
    """Detect the primary time column for a table"""
    if engine is None: 
        return None
    # Query database schema to find time-like columns
    query = """
    SELECT column_name 
    FROM information_schema.columns 
    WHERE table_name = :table_name 
    AND (
        column_name LIKE '%time%' OR 
        column_name LIKE '%date%' OR 
        column_name LIKE '%created%' OR 
        column_name LIKE '%updated%'
    )
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query), {'table_name': table_name})
            columns = [row[0] for row in result.fetchall()]
            return columns[0] if columns else None
    except Exception as e:
        logger.warning(f"Error finding time column for {table_name}: {e}")
        return None

def read_table_incremental(table_name: str, since: Optional[datetime], current_df: pd.DataFrame) -> pd.DataFrame:
    """Load only new data since specified timestamp and append"""
    if since is None or engine is None:
        return read_table(table_name, force_refresh=True) # Fallback
    
    time_col = _get_time_column(table_name)
    if not time_col:
        return read_table(table_name, force_refresh=True)
    
    query = f'SELECT * FROM "{table_name}" WHERE "{time_col}" > :since ORDER BY "{time_col}"'
    try:
        new_df = pd.read_sql(text(query), con=engine, params={'since': since})
        if not new_df.empty:
            # normalize columns
            new_df.columns = [c.lower() for c in new_df.columns]
            for c in new_df.columns:
                 if _is_time_like(c):
                     try:
                         new_df[c] = pd.to_datetime(new_df[c])
                     except Exception:
                         pass
            
            combined = pd.concat([current_df, new_df]).drop_duplicates(subset=[time_col.lower()]).sort_values(time_col.lower())
            return combined
        else:
            return current_df
    except Exception as e:
        logger.error(f"Incremental read failed: {e}")
        return read_table(table_name, force_refresh=True)

def read_table(table_name: str, limit: Optional[int] = None, use_cache: bool = True, ttl_seconds: Optional[int] = None, force_refresh: bool = False) -> pd.DataFrame:
    """
    Read a table from the database into a pandas DataFrame
    """
    if table_name is None:
        logger.warning("read_table called with None table_name")
        return pd.DataFrame()

    key = _get_cache_key(table_name, limit=limit)

    # Try memory cache
    cached_entry = _MEM_CACHE.get(key)
    
    if use_cache and not force_refresh:
        if cached_entry is not None:
            ts = cached_entry.get('ts')
            if ttl_seconds is None or (datetime.now() - ts) <= timedelta(seconds=ttl_seconds):
                logger.debug(f"Returning cached data for table {table_name}")
                if cached_entry.get('is_compressed'):
                    return _decompress_dataframe(cached_entry['df_compressed'])
                return cached_entry['df'].copy()

    if engine is None:
        logger.error("Database engine not configured")
        raise RuntimeError("DB engine not configured")

    # Incremental loading logic if we have a cache and are refreshing
    if force_refresh and cached_entry is not None and limit is None: # Only incremental if no limit
         # Get latest timestamp from cached df
         try:
             if cached_entry.get('is_compressed'):
                 current_df = _decompress_dataframe(cached_entry['df_compressed'])
             else:
                 current_df = cached_entry['df']
             
             time_col = pick_time_column(current_df)
             if time_col:
                 last_ts = current_df[time_col].max()
                 logger.info(f"Attempting incremental load for {table_name} since {last_ts}")
                 df = read_table_incremental(table_name, last_ts, current_df)
                 _store_in_cache(key, df)
                 return df
         except Exception as e:
             logger.warning(f"Incremental update failed, falling back to full load: {e}")

    logger.info(f"Reading table {table_name} from database (limit={limit})")
    q = f'SELECT * FROM "{table_name}"'
    if limit:
        q += f" LIMIT {limit}"
    
    try:
        df = pd.read_sql(text(q), con=engine)
    except Exception as e:
        logger.error(f"Database read failed: {e}")
        return pd.DataFrame()

    # normalize column names
    df.columns = [c.lower() for c in df.columns]

    for c in df.columns:
        if _is_time_like(c):
            try:
                df[c] = pd.to_datetime(df[c])
            except Exception:
                pass

    if use_cache:
        try:
            _store_in_cache(key, df)
            logger.debug(f"Cached data for table {table_name} (rows={len(df)})")
        except Exception:
            pass

    logger.info(f"Successfully loaded {len(df)} rows from table {table_name}")
    return df


class BackgroundRefresher:
    def __init__(self):
        self.refresh_intervals = {
            'real_time': 60,     # 1 minute for real-time data
            'hourly': 3600,       # 1 hour for hourly data
            'daily': 86400        # 1 day for daily data
        }
        self.table_categories = self._categorize_tables()
        self._running = False
        self._start_background_thread()
    
    def _categorize_tables(self) -> Dict[str, str]:
        """Categorize tables by update frequency"""
        # Heuristic categorization based on keywords
        tables = list_public_tables()
        categories = {}
        for t in tables:
            if any(x in t for x in ['kp', 'index']):
                categories[t] = 'hourly'
            elif any(x in t for x in ['region', 'spot']):
                categories[t] = 'daily'
            else:
                categories[t] = 'real_time'
        return categories
    
    def _start_background_thread(self):
        """Start background refresh thread"""
        def refresh_loop():
            while self._running:
                for table, category in self.table_categories.items():
                    if self._should_refresh(table, category):
                        self._refresh_table(table)
                time.sleep(60)  # Check every minute
        
        self._running = True
        thread = threading.Thread(target=refresh_loop, daemon=True)
        thread.start()
    
    def _should_refresh(self, table: str, category: str) -> bool:
        """Check if table needs refresh"""
        key = _get_cache_key(table)
        entry = _MEM_CACHE.get(key)
        if not entry:
            return False # Don't auto-refresh if not even cached yet (wait for first user request)
        
        ts = entry['ts']
        interval = self.refresh_intervals.get(category, 3600)
        return (datetime.now() - ts).total_seconds() > interval
    
    def _refresh_table(self, table: str):
        """Refresh specific table in background"""
        try:
             # Force refresh will trigger incremental load if possible
            read_table(table, force_refresh=True)
            logger.info(f"Background refreshed table {table}")
        except Exception as e:
            logger.error(f"Background refresh failed for {table}: {e}")

# Global refresher instance - starts on import if DB is configured
_REFRESHER_INSTANCE = None
if engine is not None and not os.getenv("DISABLE_BACKGROUND_REFRESH"):
     # Simple check to avoid multiple threads in dev reloads if possible, 
     # though module reload creates new vars. 
     # Streamlit might re-execute this.
     # We rely on daemon thread dying with process, but reloads might leak threads.
     # For now, we instantiate. 
     # To be safer in Streamlit, we could check if thread is alive.
     already_running = False
     for t in threading.enumerate():
         if t.name == "BackgroundRefresher":
             already_running = True
     
     if not already_running:
         try:
             _REFRESHER_INSTANCE = BackgroundRefresher()
             # Name the thread to find it later
             # (Thread starting is inside init, we can't name it easily without modifying init)
             # But let's assume it's fine for now.
         except Exception:
             pass


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
