from typing import Optional
import streamlit as st
import plotly.express as px
import pandas as pd
import logging

try:
    from db import find_table_like, read_table
except Exception:
    from dashboard.db import find_table_like, read_table

from plot_utils import set_layout, add_download_button

logger = logging.getLogger(__name__)


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None) -> pd.DataFrame:
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
    Render solar regions section

    :param limit:
    :type limit: Optional[int]
    :return:
    """
    logger.info(f"Rendering solar regions page (limit={limit})")
    st.title('Active Solar Regions')
    tname = find_table_like(['solar','region']) or find_table_like(['solarregions'])
    logger.debug(f"Found solar regions table: {tname}")
    df = _load_table_cached(tname, limit) if tname else pd.DataFrame()
    if df.empty:
        st.info('No data for SolarRegions')
        return

    # observed date as date type
    date_col = None
    for c in df.columns:
        if 'observed' in c or 'date' in c:
            date_col = c
            break
    if date_col:
        df['observed_date'] = pd.to_datetime(df[date_col]).dt.date

    if 'area' in df.columns and 'observed_date' in df.columns:
        st.subheader('Evolution of Active Region Area')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A line chart showing the changes in the mean area of active solar regions 
            over time, calculated as the average area of all active regions observed on a given day.
            
            **Purpose of the plot:** To identify periods of increased solar activity through area growth, 
            which may indicate the development of magnetic activity and increased probability of solar flares.
            
            **Variables:**
            - **Observation date**: Date of solar region area measurement
            - **Mean Area [μhem]**: Mean area of active regions expressed in millionths of the solar hemisphere (micro-hemispheres)
            
            **Interpretation:**
            - **Area growth**: Indicates magnetic activity development and potentially higher probability of flares
            - **Stable area**: Regions persist over time, may be sources of repeated flares
            - **Area decrease**: Regions decay, solar activity decreases
            ''')

        area_ts = df.groupby('observed_date')['area'].mean().reset_index()
        fig2 = px.line(area_ts, x='observed_date', y='area', labels={'observed_date':'Observation date','area':'Mean Area [μhem]'})
        set_layout(fig2, rangeslider=True, tcol_data=area_ts['observed_date'])
        st.plotly_chart(fig2, width='stretch')
        add_download_button(area_ts, "solar_regions_areas_evolution", "Download chart data as CSV")

    if 'observed_date' in df.columns:
        st.subheader('Statistics of Active Solar Regions')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A bar chart showing the number of active solar regions observed 
            on each day of the analyzed period.
            
            **Purpose of the plot:** To assess overall solar activity and identify periods of increased 
            magnetic activity of the Sun. Analysis of the number of active regions allows for predicting 
            the probability of solar flares and coronal mass ejections.
            
            **Variables:**
            - **Observation date**: Date of solar region observation
            - **Active Region Count**: Total number of active solar regions on a given day
            
            **Interpretation:**
            - **Higher number of regions**: Indicates a period of increased solar activity, higher 
            probability of flares and coronal mass ejections
            - **Lower number of regions**: Period of quiet solar activity
            - **Rising trend**: Indicates the rising phase of the solar cycle
            - **Falling trend**: Indicates the declining phase of the solar cycle
            ''')
        counts = df.groupby('observed_date').size().reset_index(name='count')
        fig4 = px.bar(counts, x='observed_date', y='count', labels={'observed_date':'Observation date','count':'Active Region Count'})
        st.plotly_chart(fig4, width='stretch')
        add_download_button(counts, "solar_regions_statistics", "Download chart data as CSV")
