from typing import Optional, Union
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import logging

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

try:
    from plot_utils import set_layout, add_gray_areas_empty, add_download_button
except Exception:
    from dashboard.plot_utils import set_layout, add_gray_areas_empty, add_download_button

logger = logging.getLogger(__name__)


def _parse_energy_val(e: Union[str, float, int, None]) -> float:
    """
    Parse energy value from string or number

    :param e:
    :type e: Union[str, float, int, None]
    :return:
    :rtype: float
    """
    if pd.isna(e):
        return np.nan
    if isinstance(e, (int, float)):
        return float(e)
    s = str(e)
    m = ''.join(ch if (ch.isdigit() or ch=='.') else ' ' for ch in s)
    parts = [p for p in m.split() if p]
    return float(parts[0]) if parts else np.nan


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None):
    """
    Load table with caching

    :param name:
    :type name: str
    :param limit:
    :type limit: Optional[int]
    :return:
    """
    return read_table(name, limit=limit)


def render(limit: Optional[int] = None):
    """
    Render proton radiation (integral fluxes) section

    :param limit:
    :type limit: Optional[int]
    :return:
    """
    logger.info(f"Rendering protons page (limit={limit})")
    st.title('Proton Radiation — Integral Fluxes')
    p_tab = find_table_like(['primary','integral','proton'])
    s_tab = find_table_like(['secondary','integral','proton'])
    logger.debug(f"Found primary proton table: {p_tab}, secondary: {s_tab}")
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Primary Data Source', df_p), ('Secondary Data Source', df_s)):
        if df.empty:
            st.info(f'No data: {name} Integral Protons')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Proton Fluxes by Energy')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A chart showing the temporal changes in proton flux (charged particles) 
            originating from the Sun and outer space in various energy bands.
            
            **Purpose of the plot:** To monitor proton radiation levels, which can pose 
            a threat to astronauts, satellites, and electronic systems.
            
            **Variables:**
            - **Observation date**: Time of proton flux measurement
            - **Flux [cm⁻²·s⁻¹]**: Number of protons passing through a 1 cm² area per second
            - **Energy**: Proton energy band (if available in the data)
            
            **Interpretation:**
            - **Low-energy protons**: Originate mainly from the Sun, associated with solar flares
            - **High-energy protons**: Originate from outer space, can cause increased 
            radiation at aviation altitudes
            - **Sudden flux increases**: Indicate solar flares or coronal mass ejections
            ''')
        if 'energy' in df.columns:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, color='energy',
                          labels={tcol: 'Observation date', ycol: 'Flux [pfu]', 'energy': 'Proton Energy'}, log_y=True, markers=True, color_discrete_sequence=px.colors.qualitative.Dark24)
            fig.update_traces(line=dict(width=2), marker=dict(size=5))
            set_layout(fig, f'{name} — Proton Fluxes by Energy', rangeslider=True, legend_title_text="Proton Energy", tcol_data=df[tcol])
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Observation date', ycol: 'Proton Flux [pfu]', 'energy': 'Proton Energy'}, log_y=True, markers=True)
            fig.update_traces(line=dict(width=1.8), marker=dict(size=4))
            set_layout(fig, f'{name} — Proton Fluxes', rangeslider=True, legend_title_text="Proton Energy", tcol_data=df[tcol])

        add_gray_areas_empty(fig, df, tcol)
        fig.update_layout(
            hoverlabel=dict(
                font=dict(size=10)
            )
        )
        st.plotly_chart(fig, width='stretch')
        download_df = df.copy()
        source_suffix = "primary" if name == 'Primary Data Source' else "secondary"
        add_download_button(download_df, f"protons_{source_suffix}", "Download chart data as CSV")
