import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

from plot_utils import set_layout, add_gray_areas_empty


@st.cache_data(ttl=600)
def _load_table_cached(name, limit):
    return read_table(name, limit=limit)


def _label_for_col(c: str) -> str:
    lc = c.lower()
    if 'bt' in lc and not any(x in lc for x in ('bx','by','bz')):
        return 'Bt (całkowite) [nT]'
    if 'bx' in lc:
        return 'Bx (GSM) [nT]'
    if 'by' in lc:
        return 'By (GSM) [nT]'
    if 'bz' in lc:
        return 'Bz (GSM) [nT]'
    # fallback: prettify
    return c.replace('_', ' ').title()


def render(limit=None):
    st.title("Pole magnetyczne (DSCOVR)")
    table_name = find_table_like(["dscovr", "mag"]) or find_table_like(["magnetometer"]) or find_table_like(["dscovr"])
    df = _load_table_cached(table_name, limit) if table_name else pd.DataFrame()
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
        # build nice labels mapping and rename for plotting
        name_map = {c: _label_for_col(c) for c in comps}
        fig = px.line(df.sort_values(tcol), x=tcol, y=comps, labels={tcol: 'Czas'}, color_discrete_sequence=px.colors.qualitative.Set2)
        # update trace names
        for tr in fig.data:
            orig = tr.name
            if orig in name_map:
                tr.name = name_map[orig]
        fig.update_traces(mode='lines', line=dict(width=1.8))
        set_layout(fig, 'Składniki pola: Bt, Bx, By, Bz')

        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(df.head())

    bzg = None
    for c in df.columns:
        if 'bz_gsm' in c or c == 'bz' or c.endswith('bz'):
            bzg = c
            break
    if bzg:
        st.subheader('Histogram — rozkład BzGsm')
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje rozkład wartości składowej pola magnetycznego w osi Z w układzie GSM (BzGsm). 
            Histogram pozwala ocenić częstość występowania wartości dodatnich i ujemnych Bz.
            ''')
        fig2 = px.histogram(df, x=bzg, nbins=80, labels={bzg: 'Bz (GSM) [nT]'}, color_discrete_sequence=['#636EFA'])
        set_layout(fig2, 'Rozkład BzGsm', rangeslider=False)
        st.plotly_chart(fig2, use_container_width=True)
