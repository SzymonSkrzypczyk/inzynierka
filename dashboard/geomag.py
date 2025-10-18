import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


def _detect_k_column(df):
    for c in df.columns:
        if c in ("kpindex", "kp_index", "kp") or c.endswith("kpindex"):
            return c
    nums = df.select_dtypes("number").columns.tolist()
    return nums[0] if nums else None


def render(limit=None):
    st.title("Geomagnetyzm")
    st.subheader("Planetarny i lokalny K-index")

    # Planetary Kp
    p_table = find_table_like(["planetary", "k"]) or find_table_like(["k", "index"])
    df_p = read_table(p_table, limit=limit) if p_table else pd.DataFrame()
    if not df_p.empty:
        tcol = pick_time_column(df_p)
        ycol = _detect_k_column(df_p)
        st.markdown("#### Planetarny Kp — wykres czasowy")
        if tcol and ycol:
            fig = px.line(df_p.sort_values(tcol), x=tcol, y=ycol, labels={tcol: "Czas", ycol: "Kp"})
            st.plotly_chart(fig, use_container_width=True)

            # heatmap day vs hour
            df_p['date'] = pd.to_datetime(df_p[tcol]).dt.date
            df_p['hour'] = pd.to_datetime(df_p[tcol]).dt.hour
            pivot = df_p.groupby(['date','hour'])[ycol].mean().reset_index()
            heat = pivot.pivot(index='date', columns='hour', values=ycol).fillna(0)
            st.markdown('#### Heatmap — intensywność KpIndex (średnia)')
            fig2 = px.imshow(heat, labels=dict(x='Godzina', y='Data', color='Kp'), aspect='auto')
            st.plotly_chart(fig2, use_container_width=True)

            # scatter for storms
            storms = df_p[df_p[ycol] >= 5]
            if not storms.empty:
                st.markdown('#### Burze geomagnetyczne — Kp >= 5')
                fig3 = px.scatter(storms, x=tcol, y=ycol, color=ycol, labels={tcol: 'Czas', ycol: 'Kp'})
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.write(df_p.head())
    else:
        st.info("Brak danych Planetary Kp")

    # Boulder K
    b_table = find_table_like(["boulder"]) or find_table_like(["boulder", "k"])
    df_b = read_table(b_table, limit=limit) if b_table else pd.DataFrame()
    if not df_b.empty:
        tcol = pick_time_column(df_b)
        ycol = None
        for c in df_b.columns:
            if c in ("kindex", "k_index", "k"):
                ycol = c
                break
        if not ycol:
            nums = df_b.select_dtypes("number").columns.tolist()
            ycol = nums[0] if nums else None
        st.markdown("#### Boulder K-index — wykres czasowy")
        if tcol and ycol:
            fig = px.line(df_b.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'K-index'})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(df_b.head())
    else:
        st.info("Brak danych Boulder K-index")
