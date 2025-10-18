import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


def render(limit=None):
    st.title("Pole magnetyczne (DSCOVR)")
    tname = find_table_like(["dscovr", "mag"]) or find_table_like(["magnetometer"]) or find_table_like(["dscovr"])
    df = read_table(tname, limit=limit) if tname else pd.DataFrame()
    if df.empty:
        st.info("Brak danych magnetometru DSCOVR")
        return
    tcol = pick_time_column(df)
    st.subheader("Multi-line: składniki pola")
    comps = [c for c in df.columns if any(x in c for x in ["bt", "bx", "by", "bz"]) ]
    if tcol and comps:
        fig = px.line(df.sort_values(tcol), x=tcol, y=comps, labels={tcol: 'Czas'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(df.head())

    # Histogram BzGsm
    bzg = None
    for c in df.columns:
        if 'bzgsm' in c or c == 'bz' or c.endswith('bz'):
            bzg = c
            break
    if bzg:
        st.subheader('Histogram — rozkład BzGsm')
        fig2 = px.histogram(df, x=bzg, nbins=80, labels={bzg: 'BzGsm'})
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter Bt vs BzGsm
    btcol = None
    for c in df.columns:
        if c == 'bt' or 'bt' in c:
            btcol = c
            break
    if btcol and bzg:
        st.subheader('Scatter — Bt vs BzGsm')
        fig3 = px.scatter(df, x=btcol, y=bzg, labels={btcol: 'Bt', bzg: 'BzGsm'}, trendline='ols')
        st.plotly_chart(fig3, use_container_width=True)
