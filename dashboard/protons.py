import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


def _parse_energy_val(e):
    # parse energy value from string like '10 MeV' to float 10.0
    if pd.isna(e):
        return np.nan
    if isinstance(e, (int, float)):
        return float(e)
    s = str(e)
    m = ''.join(ch if (ch.isdigit() or ch=='.') else ' ' for ch in s)
    parts = [p for p in m.split() if p]
    return float(parts[0]) if parts else np.nan


def render(limit=None):
    st.title('Protony — integralne')
    # primary and secondary
    p_tab = find_table_like(['primary','integral','proton'])
    s_tab = find_table_like(['secondary','integral','proton'])
    df_p = read_table(p_tab, limit=limit) if p_tab else pd.DataFrame()
    df_s = read_table(s_tab, limit=limit) if s_tab else pd.DataFrame()

    # Multi-line: time vs flux separated by energy
    for name, df in (('Primary', df_p), ('Secondary', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} Integral Protons')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Flux według Energy (multi-line)')
        if 'energy' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0], color='energy', labels={tcol: 'Czas', 'flux': 'Flux'}, log_y=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Flux'}, log_y=True)
            st.plotly_chart(fig, use_container_width=True)

    if not df_p.empty:
        st.subheader('Spektralny wykres log–log (Energy vs Flux) — wybierz dzień')
        if 'energy' in df_p.columns:
            df_p['energy_val'] = df_p['energy'].apply(_parse_energy_val)
            df_p['date'] = pd.to_datetime(df_p[pick_time_column(df_p)]).dt.date
            dates = df_p['date'].dropna().unique()
            if len(dates) > 0:
                sel = st.selectbox('Wybierz datę', sorted(dates, reverse=True))
                sp = df_p[df_p['date'] == sel]
                if not sp.empty:
                    x = sp['energy_val']
                    y = sp['flux'] if 'flux' in sp.columns else sp.select_dtypes('number').columns[0]
                    fig = px.scatter(sp, x=x, y=y, log_x=True, log_y=True, labels={'x': 'Energy', 'y': 'Flux'})
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info('Brak danych dla wybranej daty')
            else:
                st.info('Brak rozpoznawalnych dat w danych')
