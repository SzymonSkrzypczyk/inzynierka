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
    st.title("Pole magnetyczne międzyplanetarne (DSCOVR)")
    table_name = find_table_like(["dscovr", "mag"]) or find_table_like(["magnetometer"]) or find_table_like(["dscovr"])
    df = _load_table_cached(table_name, limit) if table_name else pd.DataFrame()
    if df.empty:
        st.info("Brak danych magnetometru DSCOVR")
        return
    tcol = pick_time_column(df)
    st.subheader("Składniki pola magnetycznego międzyplanetarnego")
    with st.expander('Opis'):
        st.markdown('''
        **Pole magnetyczne międzyplanetarne** mierzone przez satelitę DSCOVR w punkcie Lagrange'a L1 
        (1,5 mln km od Ziemi w kierunku Słońca). Dane przedstawiają składniki pola magnetycznego w układzie 
        współrzędnych GSM (Geocentric Solar Magnetospheric): Bt (całkowite), Bx, By, Bz. 
        Szczególnie ważna jest składowa Bz - jej orientacja południowa (ujemna) sprzyja 
        przenikaniu energii słonecznej do magnetosfery Ziemi i wywoływaniu burz geomagnetycznych.
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
        set_layout(fig, 'Składniki pola magnetycznego międzyplanetarnego (DSCOVR)')

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
        st.subheader('Rozkład statystyczny składowej Bz')
        with st.expander('Opis'):
            st.markdown('''
            **Histogram składowej Bz** pokazuje rozkład wartości pola magnetycznego w osi Z układu GSM. 
            Składowa Bz jest kluczowa dla procesów sprzężenia magnetosfera-wiatr słoneczny. 
            Wartości ujemne (południowe) Bz sprzyjają efektywnemu przenikaniu energii słonecznej 
            do magnetosfery Ziemi, podczas gdy wartości dodatnie (północne) działają ochronnie. 
            Analiza rozkładu pozwala ocenić dominujące warunki wiatru słonecznego.
            ''')
        fig2 = px.histogram(df, x=bzg, nbins=80, labels={bzg: 'Bz (GSM) [nT]'}, color_discrete_sequence=['#636EFA'])
        set_layout(fig2, 'Rozkład statystyczny składowej Bz (GSM)', rangeslider=False)
        st.plotly_chart(fig2, use_container_width=True)
