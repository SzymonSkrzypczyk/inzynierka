from typing import Optional
import streamlit as st
import plotly.express as px
import pandas as pd
import logging

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

from plot_utils import set_layout, add_gray_areas_empty, add_download_button

logger = logging.getLogger(__name__)


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
        return 'Bt (Total) [nT]'
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
    logger.info(f"Rendering magnetic field page (limit={limit})")
    st.title("Interplanetary Magnetic Field (DSCOVR)")
    table_name = find_table_like(["dscovr", "mag"]) or find_table_like(["magnetometer"]) or find_table_like(["dscovr"])
    logger.debug(f"Found magnetic field table: {table_name}")
    df = _load_table_cached(table_name, limit) if table_name else pd.DataFrame()
    if df.empty:
        st.info("No DSCOVR magnetometer data")
        return
    tcol = pick_time_column(df)
    st.subheader("Components of the Interplanetary Magnetic Field")
    with st.expander('Description'):
        st.markdown('''
        **Description:** A chart showing the temporal changes in the components of the interplanetary 
        magnetic field measured by the DSCOVR satellite at the Lagrange point L1 (1.5 million km from Earth towards the Sun).
        
        **Purpose of the plot:** To monitor solar wind conditions and identify moments conducive 
        to the occurrence of geomagnetic storms. Analysis of magnetic field changes allows predicting 
        the impact of solar wind on Earth's magnetosphere.
        
        **Variables:**
        - **Bt (Total) [nT]**: Total magnetic field induction value in the GSM system
        - **Bx (GSM) [nT]**: Magnetic field component along the X axis of the GSM system (Sun-Earth direction)
        - **By (GSM) [nT]**: Magnetic field component along the Y axis of the GSM system (perpendicular to the ecliptic plane)
        - **Bz (GSM) [nT]**: Magnetic field component along the Z axis of the GSM system (perpendicular to the Sun-Earth axis)
        - **Observation date**: Time of measurement

        ''')
    comps = [c for c in df.columns if any(x in c for x in ["bt", "bx", "by", "bz"]) ]
    if tcol and comps:
        # build nice labels mapping and rename for plotting
        name_map = {c: _label_for_col(c) for c in comps}
        fig = px.line(df.sort_values(tcol), x=tcol, y=comps, labels={tcol: 'Observation date', 'variable': 'Component'}, color_discrete_sequence=px.colors.qualitative.Set2)
        # update trace names
        for tr in fig.data:
            orig = tr.name
            if orig in name_map:
                tr.name = name_map[orig]
        fig.update_traces(mode='lines', line=dict(width=1.8))
        set_layout(fig, 'Interplanetary Magnetic Field Components (DSCOVR)', legend_title_text='Magnetic Field Components',
                   rangeslider=True, yaxis_title='Magnetic Field Induction [nT]', tcol_data=df[tcol])

        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, width='stretch')
        download_cols = [tcol] + comps if tcol and comps else df.columns.tolist()
        download_df = df[download_cols].copy()
        add_download_button(download_df, "magnetic_field_dscovr", "Download chart data as CSV")
    else:
        st.write(df.head())

    bzg = None
    for c in df.columns:
        if 'bz_gsm' in c or c == 'bz' or c.endswith('bz'):
            bzg = c
            break
    if bzg:
        st.subheader('Statistical Distribution of Bz Component')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A histogram showing the statistical distribution of the Bz component of the 
            interplanetary magnetic field over the analyzed time period.
            
            **Purpose of the plot:** To assess dominant solar wind conditions and identify the frequency 
            of Bz values conductive to geomagnetic storms. Analysis of the distribution helps understand 
            the statistical characteristics of the magnetic field over a long period.
            
            **Variables:**
            - **Bz (GSM) [nT]**: Value of the Z component of the magnetic field in the GSM coordinate system
            - **Count in range**: Number of occurrences of a given Bz value in the analyzed period
            
            **Interpretation:** 
            - Negative (southward) Bz values favor effective transfer of solar energy 
            into Earth's magnetosphere
            - Positive (northward) Bz values act protectively and reduce coupling efficiency
            - A distribution with a prevalence of negative values indicates periods of increased geomagnetic activity
            ''')
        fig2 = px.histogram(df, x=bzg, nbins=15, labels={bzg: 'Bz (GSM) [nT]'}, color_discrete_sequence=['#636EFA'])
        set_layout(fig2, 'Statistical Distribution of Bz Component (GSM)', rangeslider=False, yaxis_title="Count in range")
        st.plotly_chart(fig2, width='stretch')
        download_df = df[[bzg]].copy() if bzg else df.copy()
        add_download_button(download_df, "bz_distribution", "Download chart data as CSV")
