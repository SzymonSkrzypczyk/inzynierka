import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

try:
    from plot_utils import set_layout, add_gray_areas_empty
except Exception:
    from dashboard.plot_utils import set_layout, add_gray_areas_empty


def _parse_energy_val(e):
    if pd.isna(e):
        return np.nan
    if isinstance(e, (int, float)):
        return float(e)
    s = str(e)
    m = ''.join(ch if (ch.isdigit() or ch=='.') else ' ' for ch in s)
    parts = [p for p in m.split() if p]
    return float(parts[0]) if parts else np.nan


@st.cache_data(ttl=600)
def _load_table_cached(name, limit):
    return read_table(name, limit=limit)


def render(limit=None):
    st.title('Promieniowanie protonowe — strumienie integralne')
    p_tab = find_table_like(['primary','integral','proton'])
    s_tab = find_table_like(['secondary','integral','proton'])
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Primary', df_p), ('Secondary', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} Integral Protons')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Strumienie protonowe według energii')
        with st.expander('Opis'):
            st.markdown('''
            **Strumienie protonowe** przedstawiają intensywność promieniowania kosmicznego pochodzącego 
            od Słońca w różnych pasmach energetycznych. Protony o wysokiej energii mogą stanowić 
            zagrożenie dla astronautów, satelitów i systemów elektronicznych. Wykres pokazuje 
            zmiany strumienia w czasie dla różnych energii - od niskoenergetycznych protonów 
            słonecznych po wysokoenergetyczne cząstki kosmiczne.
            ''')
        if 'energy' in df.columns:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, color='energy', labels={tcol: 'Czas', ycol: 'Strumień [cm⁻²·s⁻¹]'}, log_y=True, markers=True, color_discrete_sequence=px.colors.qualitative.Dark24)
            fig.update_traces(line=dict(width=2), marker=dict(size=5))
            set_layout(fig, f'{name} — Strumienie protonowe według energii', rangeslider=True)
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Strumień [cm⁻²·s⁻¹]'}, log_y=True, markers=True)
            fig.update_traces(line=dict(width=1.8), marker=dict(size=4))
            set_layout(fig, f'{name} — Strumienie protonowe', rangeslider=True)

        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, use_container_width=True)
