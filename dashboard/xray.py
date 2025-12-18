from typing import Optional
import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column
from plot_utils import set_layout, add_gray_areas_empty, add_download_button


def _classify_flux(v: float) -> str:
    """
    Classify solar flare based on X-ray flux value
    Values based on https://www.swpc.noaa.gov/phenomena/solar-flares-radio-blackouts

    :param v:
    :type v: float
    :return:
    :rtype: str
    """
    try:
        v = float(v)
    except Exception:
        return 'Unknown'
    if v <= 0:
        return 'Unknown'
    elif v >= 1e-4:
        return 'X'
    elif v >= 1e-5:
        return 'M'
    elif v >= 1e-6:
        return 'C'
    elif v >= 1e-7:
        return 'B'
    return 'A'


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None):
    """
    Load table from database with caching

    :param name:
    :type name: str
    :param limit:
    :type limit: Optional[int]
    :return:
    """
    return read_table(name, limit=limit)


def render(limit: Optional[int] = None):
    """
    Render solar X-ray radiation section

    :param limit:
    :type limit: Optional[int]
    :return:
    """
    st.title('Promieniowanie rentgenowskie Słońca')
    p_tab = find_table_like(['primary','xray'])
    s_tab = find_table_like(['secondary','xray'])
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Główny źródło danych', df_p), ('Zapasowe źródło danych', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} X-ray')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Strumienie promieniowania X według satelity')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres liniowy przedstawiający czasowe zmiany strumienia promieniowania 
            rentgenowskiego emitowanego przez Słońce w różnych pasmach energetycznych, mierzonego 
            przez satelity GOES-18 i GOES-19 monitorujące aktywność słoneczną.
            
            **Cel wykresu:** Monitorowanie aktywności słonecznej poprzez pomiar promieniowania 
            rentgenowskiego, które jest emitowane podczas rozbłysków słonecznych i aktywności 
            koronalnej.
            
            **Zmienne:**
            - **Data obserwacji**: Moment pomiaru strumienia promieniowania X
            - **Strumień [W·m⁻²]**: Moc promieniowania rentgenowskiego na jednostkę powierzchni
            - **Satelita**: Satelita dokonujący pomiaru
            
            **Pasma energetyczne:**
            - **Primary**: Promieniowanie twarde (wysoka energia)
            - **Secondary**: Promieniowanie miękkie (niższa energia)
            
            **Interpretacja:** Nagłe wzrosty strumienia wskazują na rozbłyski słoneczne. Wykres 
            wykorzystuje skalę logarytmiczną ze względu na bardzo szeroki zakres wartości strumienia.
            ''')
        if 'satellite' in df.columns and 'flux' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux', color='satellite', labels={tcol:'Data obserwacji','flux':'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.6))
            set_layout(fig, f'{name} — Strumienie promieniowania X według satelity', legend_title_text="Satelita", tcol_data=df[tcol])
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol:'Data obserwacji', ycol:'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=['#636EFA'])
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.4))
            set_layout(fig, f'{name} — Strumienie promieniowania X', tcol_data=df[tcol])


        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, width='stretch')
        download_df = df.copy()
        source_suffix = "glowny" if name == 'Główny źródło danych' else "zapasowy"
        add_download_button(download_df, f"promieniowanie_x_{source_suffix}", "Pobierz dane z wykresu jako CSV")

        if 'flux' in df.columns:
            st.subheader('Klasyfikacja rozbłysków słonecznych')
            with st.expander('Opis'):
                st.markdown('''
                **Opis:** Wykres punktowy przedstawiający wszystkie pomiary strumienia promieniowania 
                rentgenowskiego sklasyfikowane według klasy rozbłysku słonecznego.
                
                **Cel wykresu:** Identyfikacja i klasyfikacja rozbłysków słonecznych według ich 
                intensywności oraz ocena ryzyka dla systemów technicznych na Ziemi i w przestrzeni 
                kosmicznej.
                
                **Zmienne:**
                - **Data obserwacji**: Moment pomiaru strumienia promieniowania X
                - **Strumień [W·m⁻²]**: Moc promieniowania rentgenowskiego na jednostkę powierzchni
                - **Klasa rozbłysku**: Klasyfikacja rozbłysku według intensywności (A, B, C, M, X)
                
                **Klasyfikacja rozbłysków:**
                - **Klasa A**: < 10⁻⁷ W·m⁻² (bardzo słabe, tło słoneczne)
                - **Klasa B**: 10⁻⁷ – 10⁻⁶ W·m⁻² (bardzo słabe, tło słoneczne)
                - **Klasa C**: 10⁻⁶ - 10⁻⁵ W·m⁻² (słabe, niewielki wpływ na Ziemię)
                - **Klasa M**: 10⁻⁵ - 10⁻⁴ W·m⁻² (umiarkowane, mogą powodować krótkotrwałe zakłócenia radiowe)
                - **Klasa X**: >= 10⁻⁴ W·m⁻² (silne, mogą powodować poważne zakłócenia w komunikacji 
                radiowej, systemach nawigacyjnych i sieciach energetycznych)
                
                **Kolory:** X (czerwony), M (pomarańczowy), C (niebieski), B (brązowy), A (zielony), Nieznany (szary)
                ''')
            df['flare_class'] = df['flux'].apply(_classify_flux)
            fig2 = px.scatter(df, x=tcol, y='flux', color='flare_class', labels={tcol:'Data obserwacji','flux':'Strumień [W·m⁻²]'}, log_y=True,
                              color_discrete_map={'X':'#7f0000','M':'#ff7f0e','C':'#1f77b4','B':'#8c564b','A':'#2ca02c','Unknown':'#d3d3d3'})
            fig2.update_traces(marker=dict(size=6))
            set_layout(fig2, f'{name} — Klasyfikacja rozbłysków słonecznych', legend_title_text="Klasa rozbłysku", tcol_data=df[tcol])
            add_gray_areas_empty(fig2, df, tcol)
            st.plotly_chart(fig2, width='stretch')
            download_df = df[[tcol, 'flux', 'flare_class']].copy() if tcol and 'flux' in df.columns else df.copy()
            add_download_button(download_df, f"klasyfikacja_rozblyskow_{source_suffix}", "Pobierz dane z wykresu jako CSV")

        pk_tab = find_table_like(['planetary','kp']) or find_table_like(['kp','index'])
        df_k = _load_table_cached(pk_tab, limit) if pk_tab else pd.DataFrame()

        st.subheader('Rozkład wartości strumieni promieniowania X')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Histogram przedstawiający rozkład statystyczny wartości strumienia promieniowania 
            rentgenowskiego w analizowanym okresie czasowym.
            
            **Cel wykresu:** Ocena ogólnej aktywności słonecznej oraz identyfikacja charakterystyk 
            rozkładu strumieni promieniowania X. Analiza pozwala zrozumieć, jak często występują 
            różne poziomy aktywności słonecznej i ocenić, czy dany okres charakteryzuje się zwiększoną 
            aktywnością słoneczną.
            
            **Zmienne:**
            - **Strumień [W·m⁻²]**: Wartość strumienia promieniowania rentgenowskiego na jednostkę powierzchni
            - **Liczba wartości w danym zakresie**: Liczba wystąpień danej wartości strumienia w analizowanym zakresie (w skali logarytmicznej)
            
            **Interpretacja:**
            - **Dominacja niskich wartości**: Większość czasu Słońce emituje niskie strumienie (klasa A/B), 
            co jest normalnym tłem słonecznym
            - **Rzadkie wysokie wartości**: Silne rozbłyski (klasa M i X) są rzadkie, ale intensywne, 
            tworząc długi "ogon" rozkładu
            - **Przesunięcie w prawo**: Rozkład z większą liczbą wyższych wartości wskazuje na okres 
            zwiększonej aktywności słonecznej (np. maksimum cyklu słonecznego)
            ''')
        fig4 = px.histogram(df, x='flux', nbins=50, labels={'flux':'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=['#00CC96'])
        set_layout(fig4, 'Rozkład wartości strumieni promieniowania X', rangeslider=False, yaxis_title="Liczba wartości w danym zakresie")
        st.plotly_chart(fig4, width='stretch')
        download_df = df[['flux']].copy() if 'flux' in df.columns else df.copy()
        add_download_button(download_df, "rozkład_promieniowania_x", "Pobierz dane z wykresu jako CSV")
