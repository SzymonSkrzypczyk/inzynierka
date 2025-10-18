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
    # try to extract numeric energy value from strings like 'E>10MeV' or '10 MeV'
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
        # energy column may be 'energy'
        if 'energy' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0], color='energy', labels={tcol: 'Czas', 'flux': 'Flux'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            # try numeric columns
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Flux'})
            st.plotly_chart(fig, use_container_width=True)

    # Log–Log spectral plot — Energy vs Flux for selected day (choose date)
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
        else:
            st.info('Brak kolumny Energy w PrimaryIntegralProtons1Day — pomiń wykres spektralny')

    # Scatter Plot — Flux (protony) vs KpIndex (z PlanetaryKIndex1m)
    # Use daily mean Kp to join
    pk_table = find_table_like(['planetary','kp']) or find_table_like(['kp','index'])
    df_k = read_table(pk_table, limit=limit) if pk_table else pd.DataFrame()
    if not df_p.empty and not df_k.empty:
        st.subheader('Scatter — Flux vs KpIndex (łączone dziennie)')
        df_p['date'] = pd.to_datetime(df_p[pick_time_column(df_p)]).dt.date
        tcol_k = pick_time_column(df_k)
        df_k['date'] = pd.to_datetime(df_k[tcol_k]).dt.date
        avg_k = df_k.groupby('date').mean().reset_index()
        # pick flux column
        fluxcol = 'flux' if 'flux' in df_p.columns else df_p.select_dtypes('number').columns[0]
        merged = df_p.merge(avg_k, on='date', how='left')
        kpcol = None
        for c in df_k.columns:
            if c in ('kpindex','kp_index','kp','kpindex') or c.endswith('kp'):
                kpcol = c
                break
        if kpcol is None:
            # fallback numeric
            kpcol = df_k.select_dtypes('number').columns[0] if not df_k.select_dtypes('number').empty else None
        if kpcol:
            fig = px.scatter(merged, x='date', y=fluxcol, color=kpcol, labels={'date':'Data', fluxcol:'Flux', kpcol:'Kp'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info('Nie znaleziono kolumny Kp w PlanetaryKIndex1m')
    else:
        st.info('Brak danych do wykresu Flux vs KpIndex')

    # Boxplot — rozkład Flux dla różnych satelitów
    if not df_p.empty and 'satellite' in df_p.columns:
        st.subheader('Boxplot — Flux per Satellite')
        fluxcol = 'flux' if 'flux' in df_p.columns else df_p.select_dtypes('number').columns[0]
        fig = px.box(df_p, x='satellite', y=fluxcol, labels={'satellite':'Satelita', fluxcol:'Flux'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info('Brak danych satelitarnych dla boxplotu')

