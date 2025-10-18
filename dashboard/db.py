from sqlalchemy import create_engine, text
import pandas as pd
import os
import re

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


def read_table(table_name, limit=None):
    if engine is None:
        raise RuntimeError("DB engine not configured (set DB_USER/DB_PASSWORD/DB_HOST/DB_NAME)")
    if table_name is None:
        return pd.DataFrame()
    q = f'SELECT * FROM "{table_name}"'
    if limit:
        q += f" LIMIT {limit}"
    df = pd.read_sql(text(q), con=engine)
    df.columns = [c.lower() for c in df.columns]
    # parse datetime-like columns
    for c in df.columns:
        if re.search(r"time|date|timetag|processedat|processed_at|observed", c):
            try:
                df[c] = pd.to_datetime(df[c])
            except Exception:
                pass
    return df


def pick_time_column(df):
    if df is None or df.empty:
        return None
    candidates = [c for c in df.columns if re.search(r"time|date|timetag|processedat|processed_at|observed", c)]
    if not candidates:
        return None
    for c in candidates:
        if "timetag" in c or c == "time" or c.endswith("_at"):
            return c
    return candidates[0]

