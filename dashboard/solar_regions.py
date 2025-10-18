import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


def render(limit=None):
    st.title('Regiony słoneczne')
    tname = find_table_like(['solar','region']) or find_table_like(['solarregions'])
    df = read_table(tname, limit=limit) if tname else pd.DataFrame()
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
        st.subheader('Regiony: Data vs Region (kolor = MagClass)')
        with st.expander('Opis'):
            st.markdown('''
            Macierz aktywnych regionów z podziałem na klasy magnetyczne. 
            Pozwala obserwować rozwój aktywności słonecznej oraz potencjalne źródła rozbłysków
            ''')
        color = 'mag_class' if 'mag_class' in df.columns else None
        fig = px.scatter(df, x='observed_date', y='region', color=color, labels={'observed_date':'Data','region':'Region','magclass':'Klasa magnetyczna'})
        st.plotly_chart(fig, use_container_width=True)

    if 'area' in df.columns and 'observed_date' in df.columns:
        st.subheader('Powierzchnia regionów w czasie')
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje zmiany łącznej powierzchni aktywnych regionów słonecznych w czasie. 
            Wykres pozwala obserwować rozwój i zanikanie aktywnych regionów
            ''')

        area_ts = df.groupby('observed_date')['area'].mean().reset_index()
        fig2 = px.line(area_ts, x='observed_date', y='area', labels={'observed_date':'Data','area':'Średnia powierzchnia'})
        st.plotly_chart(fig2, use_container_width=True)

    if 'observed_date' in df.columns:
        st.subheader('Liczba regionów aktywnych w czasie')
        with st.expander('Opis'):
            st.markdown('''
            Pokazuje liczbę aktywnych regionów słonecznych w kolejnych dniach
            ''')
        counts = df.groupby('observed_date').size().reset_index(name='count')
        fig4 = px.bar(counts, x='observed_date', y='count', labels={'observed_date':'Data','count':'Liczba regionów'})
        st.plotly_chart(fig4, use_container_width=True)
