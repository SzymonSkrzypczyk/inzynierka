from uuid import uuid4
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
    logger.info(f"Rendering X-ray page (limit={limit})")
    st.title('Solar X-Ray Radiation')
    p_tab = find_table_like(['primary','xray'])
    s_tab = find_table_like(['secondary','xray'])
    logger.debug(f"Found primary X-ray table: {p_tab}, secondary: {s_tab}")
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Primary Data Source', df_p), ('Secondary Data Source', df_s)):
        if df.empty:
            st.info(f'No data: {name} X-ray')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — X-Ray Fluxes by Satellite')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A line chart showing the temporal changes in X-ray flux 
            emitted by the Sun in various energy bands, measured by satellites GOES-18 and GOES-19 
            monitoring solar activity.
            
            **Purpose of the plot:** To monitor solar activity by measuring X-ray radiation, 
            which is emitted during solar flares and coronal activity.
            
            **Variables:**
            - **Observation date**: Time of X-ray flux measurement
            - **Flux [W·m⁻²]**: X-ray radiation power per unit area
            - **Satellite**: Satellite making the measurement
            
            **Energy Bands:**
            - **Primary**: Hard X-rays (high energy)
            - **Secondary**: Soft X-rays (lower energy)
            
            **Interpretation:** Sudden flux increases indicate solar flares. The chart 
            uses a logarithmic scale due to the very wide range of flux values.
            ''')
        if 'satellite' in df.columns and 'flux' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux', color='satellite', labels={tcol:'Observation date','flux':'Flux [W·m⁻²]', 'flare_class': 'Flare Class', 'satellite': 'Satellite'}, log_y=True, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.6))
            set_layout(fig, f'{name} — X-Ray Fluxes by Satellite', legend_title_text="Satellite", tcol_data=df[tcol])
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol:'Observation date', ycol:'Flux [W·m⁻²]'}, log_y=True, color_discrete_sequence=['#636EFA'])
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.4))
            set_layout(fig, f'{name} — X-Ray Fluxes', tcol_data=df[tcol])


        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, width='stretch')
        download_df = df.copy()
        source_suffix = "glowny" if name == 'Główny źródło danych' else "zapasowy"
        add_download_button(download_df, f"promieniowanie_x_{source_suffix}", "Download chart data as CSV")

        if 'flux' in df.columns:
            st.subheader('Solar Flare Classification')
            with st.expander('Description'):
                st.markdown('''
                **Description:** A scatter plot showing all X-ray flux measurements 
                classified by solar flare class.
                
                **Purpose of the plot:** To identify and classify solar flares by their 
                intensity and assess the risk for technical systems on Earth and in space.
                
                **Variables:**
                - **Observation date**: Time of X-ray flux measurement
                - **Flux [W·m⁻²]**: X-ray radiation power per unit area
                - **Flare Class**: Classification of the flare intensity (A, B, C, M, X)
                
                **Flare Classification:**
                - **Class A**: < 10⁻⁷ W·m⁻² (very weak, solar background)
                - **Class B**: 10⁻⁷ – 10⁻⁶ W·m⁻² (very weak, solar background)
                - **Class C**: 10⁻⁶ - 10⁻⁵ W·m⁻² (weak, minor impact on Earth)
                - **Class M**: 10⁻⁵ - 10⁻⁴ W·m⁻² (moderate, can cause brief radio blackouts)
                - **Class X**: >= 10⁻⁴ W·m⁻² (strong, can cause serious radio blackouts, 
                navigation errors, and power grid fluctuations)
                
                **Colors:** X (red), M (orange), C (blue), B (brown), A (green), Unknown (grey)
                ''')
            df['flare_class'] = df['flux'].apply(_classify_flux)
            fig2 = px.scatter(df, x=tcol, y='flux', color='flare_class', labels={tcol:'Observation date','flux':'Flux [W·m⁻²]', 'flare_class': 'Flare Class'}, log_y=True,
                              color_discrete_map={'X':'#7f0000','M':'#ff7f0e','C':'#1f77b4','B':'#8c564b','A':'#2ca02c','Unknown':'#d3d3d3'})
            fig2.update_traces(marker=dict(size=6))
            set_layout(fig2, f'{name} — Solar Flare Classification', legend_title_text="Flare Class", tcol_data=df[tcol])
            add_gray_areas_empty(fig2, df, tcol)
            st.plotly_chart(fig2, width='stretch')
            download_df = df[[tcol, 'flux', 'flare_class']].copy() if tcol and 'flux' in df.columns else df.copy()
            add_download_button(download_df, f"klasyfikacja_rozblyskow_{source_suffix}", "Download chart data as CSV")

        pk_tab = find_table_like(['planetary','kp']) or find_table_like(['kp','index'])
        df_k = _load_table_cached(pk_tab, limit) if pk_tab else pd.DataFrame()

        st.subheader('X-Ray Flux Distribution')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A histogram showing the statistical distribution of X-ray flux values 
            over the analyzed time period.
            
            **Purpose of the plot:** To assess overall solar activity and identify characteristics 
            of the X-ray flux distribution. Analysis allows understanding how frequently 
            different levels of solar activity occur and assessing if the period is characterized 
            by increased solar activity.
            
            **Variables:**
            - **Flux [W·m⁻²]**: X-ray radiation power per unit area
            - **Count in range**: Number of occurrences of a given flux value in the analyzed range (logarithmic scale)
            
            **Interpretation:**
            - **Dominance of low values**: Most of the time the Sun emits low fluxes (class A/B), 
            which is the normal solar background
            - **Rare high values**: Strong flares (class M and X) are rare but intense, 
            creating a long "tail" of the distribution
            - **Shift to the right**: A distribution with more higher values indicates a period 
            of increased solar activity (e.g., solar cycle maximum)
            ''')
        fig4 = px.histogram(df, x='flux', nbins=50, labels={'flux':'Flux [W·m⁻²]', 'count': 'count'}, log_y=True, color_discrete_sequence=['#00CC96'])
        set_layout(fig4, 'X-Ray Flux Distribution', rangeslider=False, yaxis_title="Count in range")
        st.plotly_chart(fig4, width='stretch')
        download_df = df[['flux']].copy() if 'flux' in df.columns else df.copy()
        add_download_button(download_df, f"rozkład_promieniowania_x_{str(uuid4())}", "Download chart data as CSV")
