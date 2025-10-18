import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

try:
    from plot_utils import set_layout
except Exception:
    from dashboard.plot_utils import set_layout


def _classify_flux(v):
    # Try GOES-like thresholds (W/m2). If values too large/small, fallback to quantiles
    try:
        v = float(v)
    except Exception:
        return 'Unknown'
    if v <= 0:
        return 'Unknown'
    # standard GOES thresholds
    if v >= 1e-4:
        return 'X'
    if v >= 1e-5:
        return 'M'
    if v >= 1e-6:
        return 'C'
    # fallback
    return 'A/B'


def render(limit=None):
    st.title('Promieniowanie X')
    p_tab = find_table_like(['primary','xray'])
    s_tab = find_table_like(['secondary','xray'])
    df_p = read_table(p_tab, limit=limit) if p_tab else pd.DataFrame()
    df_s = read_table(s_tab, limit=limit) if s_tab else pd.DataFrame()

    for name, df in (('Primary', df_p), ('Secondary', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} X-ray')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — TimeTag vs Flux (per satelita)')
        if 'satellite' in df.columns and 'flux' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux', color='satellite', labels={tcol:'Czas','flux':'Flux'}, log_y=True)
            fig.update_traces(mode='lines+markers', marker=dict(size=3), line=dict(width=1.5))
            set_layout(fig, f'{name} — Flux per satelita')
            st.plotly_chart(fig, use_container_width=True)
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol:'Czas', ycol:'Flux'}, log_y=True)
            fig.update_traces(mode='lines+markers', marker=dict(size=3), line=dict(width=1.4))
            set_layout(fig, f'{name} — Flux')
            st.plotly_chart(fig, use_container_width=True)

        # Threshold plot — classify
        if 'flux' in df.columns:
            st.subheader('Threshold plot — klasy rozbłysków')
            df['flare_class'] = df['flux'].apply(_classify_flux)
            fig2 = px.scatter(df, x=tcol, y='flux', color='flare_class', labels={tcol:'Czas','flux':'Flux'}, log_y=True, color_discrete_map={'X':'#7f0000','M':'#ff7f0e','C':'#1f77b4','A/B':'#8c564b','Unknown':'#d3d3d3'})
            fig2.update_traces(marker=dict(size=6), selector=dict(mode='markers'))
            set_layout(fig2, f'{name} — Klasy rozbłysków')
            st.plotly_chart(fig2, use_container_width=True)

        # Scatter Flux vs KpIndex (use planetary Kp daily average)
        pk_tab = find_table_like(['planetary','kp']) or find_table_like(['kp','index'])
        df_k = read_table(pk_tab, limit=limit) if pk_tab else pd.DataFrame()
        if not df_k.empty:
            kcol = None
            for c in df_k.columns:
                if c in ('kpindex','kp_index','kp') or c.endswith('kp'):
                    kcol = c
                    break
            if kcol is None:
                numcols = df_k.select_dtypes('number').columns
                kcol = numcols[0] if len(numcols)>0 else None
            if kcol:
                df['date'] = pd.to_datetime(df[tcol]).dt.date
                df_k['date'] = pd.to_datetime(df_k[pick_time_column(df_k)]).dt.date
                mean_k = df_k.groupby('date')[kcol].mean().reset_index()
                merged = df.merge(mean_k, on='date', how='left')
                st.subheader('Scatter — Flux vs KpIndex')
                fig3 = px.scatter(merged, x='flux', y=kcol, labels={'flux':'Flux', kcol:'Kp'}, trendline='ols', color_discrete_sequence=['#636EFA'])
                set_layout(fig3, 'Flux vs KpIndex')
                st.plotly_chart(fig3, use_container_width=True)
        # Histogram of Flux over time
        st.subheader('Histogram — rozkład Flux')
        fig4 = px.histogram(df, x='flux', nbins=80, labels={'flux':'Flux'}, log_y=True, color_discrete_sequence=['#00CC96'])
        set_layout(fig4, 'Rozkład Flux', rangeslider=False)
        st.plotly_chart(fig4, use_container_width=True)
