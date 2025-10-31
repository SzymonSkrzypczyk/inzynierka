import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table
except Exception:
    from dashboard.db import find_table_like, read_table


@st.cache_data(ttl=600)
def _load_table_cached(name, limit):
    return read_table(name, limit=limit)


def render(limit=None):
    st.title('Aktywne regiony słoneczne')
    tname = find_table_like(['solar','region']) or find_table_like(['solarregions'])
    df = _load_table_cached(tname, limit) if tname else pd.DataFrame()
    if df.empty:
        st.info('Brak danych dla SolarRegions')
        return

    # observed date as date type
    date_col = None
    for c in df.columns:
        if 'observed' in c or 'date' in c:
            date_col = c
            break
    if date_col:
        df['observed_date'] = pd.to_datetime(df[date_col]).dt.date

    # Scatter ObservedDate vs Region colored by MagClass
    if 'observed_date' in df.columns and 'region' in df.columns:
        st.subheader('Mapa aktywnych regionów słonecznych')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres punktowy przedstawiający rozmieszczenie aktywnych regionów słonecznych w czasie, 
            gdzie każdy punkt reprezentuje jeden aktywny region obserwowany w danym dniu.
            
            **Cel wykresu:** Identyfikacja i śledzenie aktywnych regionów słonecznych oraz ocena ich klasy 
            magnetycznej. Wizualizacja pozwala zobaczyć ewolucję regionów słonecznych w czasie i zidentyfikować 
            regiony o zwiększonym potencjale do generowania rozbłysków słonecznych i koronalnych wyrzutów masy.
            
            **Zmienne:**
            - **Data obserwacji**: Data, w której region był obserwowany na powierzchni Słońca
            - **Numer regionu**: Unikalny identyfikator aktywnego regionu słonecznego
            - **Klasa magnetyczna**: Klasyfikacja złożoności magnetycznej regionu (β, βγ, βγδ)
            
            **Klasy magnetyczne:**
            - **β**: Region z polami o przeciwnej polarności (bipolarny)
            - **βγ**: Region z polami o przeciwnej polarności i mieszanymi polami w jednym bipolarnym kompleksie
            - **βγδ**: Najbardziej złożony magnetycznie, mieszane pola w obszarze z plamami słonecznymi - 
            główne źródło silnych rozbłysków i koronalnych wyrzutów masy
            ''')
        color = 'mag_class' if 'mag_class' in df.columns else None
        fig = px.scatter(df, x='observed_date', y='region', color=color, labels={'observed_date':'Data obserwacji','region':'Numer regionu','mag_class':'Klasa magnetyczna'})
        st.plotly_chart(fig, use_container_width=True)

    if 'area' in df.columns and 'observed_date' in df.columns:
        st.subheader('Ewolucja powierzchni aktywnych regionów')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres liniowy przedstawiający zmiany średniej powierzchni aktywnych regionów 
            słonecznych w czasie, obliczonej jako średnia powierzchnia wszystkich aktywnych regionów 
            obserwowanych w danym dniu.
            
            **Cel wykresu:** Identyfikacja okresów zwiększonej aktywności słonecznej poprzez wzrost średniej powierzchni, który może wskazywać na 
            rozwój aktywności magnetycznej i zwiększone prawdopodobieństwo wystąpienia rozbłysków słonecznych.
            
            **Zmienne:**
            - **Data obserwacji**: Data pomiaru powierzchni regionów słonecznych
            - **Średnia powierzchnia [μhem]**: Średnia powierzchnia aktywnych regionów wyrażona w 
            milionowych częściach półkuli słonecznej (micro-hemispheres)
            
            **Interpretacja:**
            - **Wzrost powierzchni**: Wskazuje na rozwój aktywności magnetycznej i potencjalnie 
            większe prawdopodobieństwo rozbłysków
            - **Stabilna powierzchnia**: Regiony utrzymują się w czasie, mogą być źródłem powtarzających się rozbłysków
            - **Spadek powierzchni**: Regiony zanikają, aktywność słoneczna maleje
            ''')

        area_ts = df.groupby('observed_date')['area'].mean().reset_index()
        fig2 = px.line(area_ts, x='observed_date', y='area', labels={'observed_date':'Data obserwacji','area':'Średnia powierzchnia [μhem]'})
        st.plotly_chart(fig2, use_container_width=True)

    if 'observed_date' in df.columns:
        st.subheader('Statystyka aktywnych regionów słonecznych')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres słupkowy przedstawiający liczbę aktywnych regionów słonecznych obserwowanych 
            w każdym dniu analizowanego okresu.
            
            **Cel wykresu:** Ocena ogólnej aktywności słonecznej i identyfikacja okresów zwiększonej 
            aktywności magnetycznej Słońca. Analiza liczby aktywnych regionów pozwala przewidzieć prawdopodobieństwo wystąpienia rozbłysków słonecznych i koronalnych wyrzutów masy.
            
            **Zmienne:**
            - **Data obserwacji**: Dzień przeprowadzenia obserwacji regionów słonecznych
            - **Liczba aktywnych regionów**: Całkowita liczba aktywnych regionów słonecznych w danym dniu
            
            **Interpretacja:**
            - **Większa liczba regionów**: Wskazuje na okres zwiększonej aktywności słonecznej, wyższe 
            prawdopodobieństwo rozbłysków i koronalnych wyrzutów masy
            - **Mniejsza liczba regionów**: Okres spokojnej aktywności słonecznej
            - **Trend wzrostowy**: Wskazuje na fazę rosnącą cyklu słonecznego
            - **Trend spadkowy**: Wskazuje na fazę malejącą cyklu słonecznego
            ''')
        counts = df.groupby('observed_date').size().reset_index(name='count')
        fig4 = px.bar(counts, x='observed_date', y='count', labels={'observed_date':'Data obserwacji','count':'Liczba aktywnych regionów'})
        st.plotly_chart(fig4, use_container_width=True)
