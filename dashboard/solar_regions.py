import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


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
            **Aktywne regiony słoneczne** to obszary na powierzchni Słońca charakteryzujące się 
            zwiększoną aktywnością magnetyczną. Wizualizacja przedstawia rozmieszczenie regionów 
            w czasie, gdzie kolor odpowiada klasie magnetycznej (β, βγ, βγδ). Regiony o klasie βγδ 
            są najbardziej złożone magnetycznie i stanowią główne źródło rozbłysków słonecznych 
            oraz koronalnych wyrzutów masy.
            ''')
        color = 'mag_class' if 'mag_class' in df.columns else None
        fig = px.scatter(df, x='observed_date', y='region', color=color, labels={'observed_date':'Data obserwacji','region':'Numer regionu','mag_class':'Klasa magnetyczna'})
        st.plotly_chart(fig, use_container_width=True)

    if 'area' in df.columns and 'observed_date' in df.columns:
        st.subheader('Ewolucja powierzchni aktywnych regionów')
        with st.expander('Opis'):
            st.markdown('''
            **Ewolucja powierzchni regionów** pokazuje zmiany średniej powierzchni aktywnych regionów 
            słonecznych w czasie. Wzrost powierzchni może wskazywać na rozwój aktywności magnetycznej 
            i zwiększone prawdopodobieństwo wystąpienia rozbłysków. Analiza trendów pozwala przewidzieć 
            okresy zwiększonej aktywności słonecznej.
            ''')

        area_ts = df.groupby('observed_date')['area'].mean().reset_index()
        fig2 = px.line(area_ts, x='observed_date', y='area', labels={'observed_date':'Data obserwacji','area':'Średnia powierzchnia [μhem]'})
        st.plotly_chart(fig2, use_container_width=True)

    if 'observed_date' in df.columns:
        st.subheader('Statystyka aktywnych regionów słonecznych')
        with st.expander('Opis'):
            st.markdown('''
            **Liczba aktywnych regionów** w kolejnych dniach pokazuje ogólną aktywność słoneczną. 
            Większa liczba regionów oznacza zwiększoną aktywność magnetyczną Słońca i wyższe 
            prawdopodobieństwo wystąpienia rozbłysków oraz koronalnych wyrzutów masy. 
            Analiza trendów pozwala ocenić fazę cyklu słonecznego.
            ''')
        counts = df.groupby('observed_date').size().reset_index(name='count')
        fig4 = px.bar(counts, x='observed_date', y='count', labels={'observed_date':'Data obserwacji','count':'Liczba aktywnych regionów'})
        st.plotly_chart(fig4, use_container_width=True)
