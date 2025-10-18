from sqlalchemy import create_engine
import pandas as pd
import streamlit as st
import os

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_PORT = os.getenv("DB_PORT", "5432")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

@st.cache_data(ttl=600)
def load_data():
    return pd.read_sql("SELECT * FROM processing_logs LIMIT 10000", engine)

st.title("Data Processing Dashboard")
data = load_data()
st.dataframe(data)