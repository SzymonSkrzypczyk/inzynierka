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


def render(limit=None):
    st.title("Pole magnetyczne (DSCOVR)")
    tname = find_table_like(["dscovr", "mag"]) or find_table_like(["magnetometer"]) or find_table_like(["dscovr"])
    df = read_table(tname, limit=limit) if tname else pd.DataFrame()
    if df.empty:
        st.info("Brak danych magnetometru DSCOVR")
        return
    tcol = pick_time_column(df)
    st.subheader("Składniki pola magnetycznego")
    with st.expander('Opis'):
        st.markdown('''
        Analiza zmienności i korelacji składników pola magnetycznego w układzie GSM
        ''')
    comps = [c for c in df.columns if any(x in c for x in ["bt", "bx", "by", "bz"]) ]
    if tcol and comps:
        fig = px.line(df.sort_values(tcol), x=tcol, y=comps, labels={tcol: 'Czas'})
        fig.update_traces(mode='lines+markers', marker=dict(size=3), line=dict(width=1))
        set_layout(fig, 'Składniki pola: Bt, Bx, By, Bz')
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
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje rozkład wartości składowej pola magnetycznego w osi Z w układzie GSM (BzGsm). 
             Histogram pozwala ocenić, jak często występują wartości dodatnie i ujemne Bz, 
             co jest istotne w analizie geomagnetycznej, ponieważ długotrwałe ujemne 
             Bz sprzyja rekoneksji magnetosferycznej i burzom geomagnetycznym
            ''')
        fig2 = px.histogram(df, x=bzg, nbins=80, labels={bzg: 'BzGsm'}, color_discrete_sequence=['#636EFA'])
        set_layout(fig2, 'Rozkład BzGsm', rangeslider=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter Bt vs BzGsm
    btcol = None
    for c in df.columns:
        if c == 'bt' or 'bt' in c:
            btcol = c
            break
    if btcol and bzg:
        st.subheader('Scatter — Bt vs BzGsm')
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje zależność między całkowitym polem magnetycznym (Bt) a jego składową w osi Z w układzie GSM (BzGsm)
            ''')
        fig3 = px.scatter(df, x=btcol, y=bzg, labels={btcol: 'Bt', bzg: 'BzGsm'}, trendline='ols', opacity=0.7)
        set_layout(fig3, 'Bt vs BzGsm')
        st.plotly_chart(fig3, use_container_width=True)
