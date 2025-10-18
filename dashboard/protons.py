import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

try:
    from plot_utils import set_layout
except Exception:
    from dashboard.plot_utils import set_layout


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
        st.subheader(f'{name} — Flux według Energy')
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje strumień protonów (Primary i Secondary) w różnych pasmach energetycznych w czasie
            ''')
        if 'energy' in df.columns:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, color='energy', labels={tcol: 'Czas', ycol: 'Flux'}, log_y=True, markers=True, color_discrete_sequence=px.colors.qualitative.Dark24)
            fig.update_traces(line=dict(width=1.8), marker=dict(size=4))
            set_layout(fig, f'{name} — Flux według Energy', rangeslider=True)
            st.plotly_chart(fig, use_container_width=True)
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Flux'}, log_y=True, markers=True)
            fig.update_traces(line=dict(width=1.6), marker=dict(size=3))
            set_layout(fig, f'{name} — Flux', rangeslider=True)
            st.plotly_chart(fig, use_container_width=True)
