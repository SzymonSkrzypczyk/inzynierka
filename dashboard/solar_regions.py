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

    # ensure observed date as date
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
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
            ''')
        color = 'magclass' if 'magclass' in df.columns else None
        fig = px.scatter(df, x='observed_date', y='region', color=color, labels={'observed_date':'Data','region':'Region','magclass':'Klasa magnetyczna'})
        st.plotly_chart(fig, use_container_width=True)

    # Line chart: Area over time
    if 'area' in df.columns and 'observed_date' in df.columns:
        st.subheader('Powierzchnia regionów w czasie')
        with st.expander('Opis'):
            st.markdown('''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
            ''')
        # aggregate mean area per date
        area_ts = df.groupby('observed_date')['area'].mean().reset_index()
        fig2 = px.line(area_ts, x='observed_date', y='area', labels={'observed_date':'Data','area':'Średnia powierzchnia'})
        st.plotly_chart(fig2, use_container_width=True)

    # Count plot — number of regions active over time
    if 'observed_date' in df.columns:
        st.subheader('Liczba regionów aktywnych w czasie')
        with st.expander('Opis'):
            st.markdown('''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
            ''')
        counts = df.groupby('observed_date').size().reset_index(name='count')
        fig4 = px.bar(counts, x='observed_date', y='count', labels={'observed_date':'Data','count':'Liczba regionów'})
        st.plotly_chart(fig4, use_container_width=True)
