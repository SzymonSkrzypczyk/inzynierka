from typing import Optional
import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

from plot_utils import set_layout, add_gray_areas_empty, add_download_button


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None) -> pd.DataFrame:
    """
    Load table with caching

    :param name:
    :type name: str
    :param limit:
    :type limit: Optional[int]
    :return:
    :rtype: pd.DataFrame
    """
    return read_table(name, limit=limit)


def _label_for_col(col_name: str) -> str:
    """
    Generate nice label for given column name

    :param col_name:
    :type col_name: str
    :return:
    """
    lc = col_name.lower()
    if 'bt' in lc and not any(x in lc for x in ('bx','by','bz')):
        return 'Bt (całkowite) [nT]'
    if 'bx' in lc:
        return 'Bx (GSM) [nT]'
    if 'by' in lc:
        return 'By (GSM) [nT]'
    if 'bz' in lc:
        return 'Bz (GSM) [nT]'
    # fallback: prettify
    return col_name.replace('_', ' ').title()


def render(limit: Optional[int] = None):
    """
    Render the interplanetary magnetic field (DSCOVR) dashboard section

    :param limit:
    :type limit: Optional[int]
    :return:
    """
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
        **Opis:** Wykres przedstawia czasowe zmiany składników pola magnetycznego międzyplanetarnego 
        mierzone przez satelitę DSCOVR w punkcie Lagrange'a L1 (1,5 mln km od Ziemi w kierunku Słońca).
        
        **Cel wykresu:** Monitorowanie warunków wiatru słonecznego i identyfikacja momentów sprzyjających 
        wystąpieniu burz geomagnetycznych. Analiza zmian pola magnetycznego pozwala przewidzieć wpływ 
        wiatru słonecznego na magnetosferę Ziemi.
        
        **Zmienne:**
        - **Bt (całkowite) [nT]**: Całkowita wartość indukcji pola magnetycznego w układzie GSM
        - **Bx (GSM) [nT]**: Składowa pola magnetycznego w osi X układu GSM (kierunek Słońce-Ziemia)
        - **By (GSM) [nT]**: Składowa pola magnetycznego w osi Y układu GSM (prostopadła do płaszczyzny ekliptyki)
        - **Bz (GSM) [nT]**: Składowa pola magnetycznego w osi Z układu GSM (prostopadła do osi Słońce-Ziemia)
        - **Data obserwacji**: Moment pomiaru

        ''')
    comps = [c for c in df.columns if any(x in c for x in ["bt", "bx", "by", "bz"]) ]
    if tcol and comps:
        # build nice labels mapping and rename for plotting
        name_map = {c: _label_for_col(c) for c in comps}
        fig = px.line(df.sort_values(tcol), x=tcol, y=comps, labels={tcol: 'Data obserwacji'}, color_discrete_sequence=px.colors.qualitative.Set2)
        # update trace names
        for tr in fig.data:
            orig = tr.name
            if orig in name_map:
                tr.name = name_map[orig]
        fig.update_traces(mode='lines', line=dict(width=1.8))
        set_layout(fig, 'Składniki pola magnetycznego międzyplanetarnego (DSCOVR)', legend_title_text="Składowe pola magnetycznego ",
                   rangeslider=True, yaxis_title='Indukcja pola magnetycznego [nT]', tcol_data=df[tcol])

        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, width='stretch')
        download_cols = [tcol] + comps if tcol and comps else df.columns.tolist()
        download_df = df[download_cols].copy()
        add_download_button(download_df, "pole_magnetyczne_dscovr", "Pobierz dane z wykresu jako CSV")
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
            **Opis:** Histogram przedstawia rozkład statystyczny wartości składowej Bz pola magnetycznego 
            międzyplanetarnego w analizowanym okresie czasowym.
            
            **Cel wykresu:** Ocena dominujących warunków wiatru słonecznego oraz identyfikacja częstotliwości 
            występowania wartości Bz sprzyjających burzom geomagnetycznym. Analiza rozkładu pozwala zrozumieć 
            charakterystyki statystyczne pola magnetycznego w długim okresie.
            
            **Zmienne:**
            - **Bz (GSM) [nT]**: Wartość składowej Z pola magnetycznego w układzie współrzędnych GSM
            - **Liczba wartości w danym zakresie**: Liczba wystąpień danej wartości Bz w analizowanym okresie
            
            **Interpretacja:** 
            - Wartości ujemne (południowe) Bz sprzyjają efektywnemu przenikaniu energii słonecznej 
            do magnetosfery Ziemi
            - Wartości dodatnie (północne) Bz działają ochronnie i zmniejszają efektywność sprzężenia
            - Rozkład z przewagą wartości ujemnych wskazuje na okresy zwiększonej aktywności geomagnetycznej
            ''')
        fig2 = px.histogram(df, x=bzg, nbins=15, labels={bzg: 'Bz (GSM) [nT]'}, color_discrete_sequence=['#636EFA'])
        set_layout(fig2, 'Rozkład statystyczny składowej Bz (GSM)', rangeslider=False, yaxis_title="Liczba wartości w danym zakresie")
        st.plotly_chart(fig2, width='stretch')
        download_df = df[[bzg]].copy() if bzg else df.copy()
        add_download_button(download_df, "rozkład_bz", "Pobierz dane z wykresu jako CSV")
