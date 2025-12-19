from typing import Optional
import streamlit as st
import plotly.express as px
import pandas as pd
from babel.dates import format_datetime
import logging

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

from plot_utils import add_gray_areas_empty, set_layout, add_download_button

logger = logging.getLogger(__name__)


def _detect_k_column(df: pd.DataFrame):
    """
    Detect K-index column in dataframe

    :param df:
    :type df: pandas.DataFrame
    :return:
    """
    for c in df.columns:
        if c in ("kpindex", "kp_index", "kp") or c.endswith("kpindex"):
            return c
    nums = df.select_dtypes("number").columns.tolist()
    return nums[0] if nums else None


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None):
    """
    Load table from database with caching

    :param name:
    :type name: str
    :param limit:
    :type limit: int or None
    :return:
    """
    return read_table(name, limit=limit)


def render(limit: Optional[int] = None):
    """
    Render geomagnetic K-index plots

    :param limit:
    :type limit: int or None
    :return:
    """
    logger.info(f"Rendering geomagnetyzm page (limit={limit})")
    st.title("Geomagnetism")
    st.subheader("Planetary and Local K-index")

    p_table = find_table_like(["planetary", "k"]) or find_table_like(["k", "index"]) or find_table_like(["planetary","kp"])
    logger.debug(f"Found planetary K table: {p_table}")
    df_p = _load_table_cached(p_table, limit) if p_table else pd.DataFrame()
    if not df_p.empty:
        tcol = pick_time_column(df_p)
        ycol = _detect_k_column(df_p)
    st.markdown("#### Planetary Kp — Time Series")
    with st.expander('Description'):
        st.markdown('''
        **Description:** A line chart showing the changes in the planetary geomagnetic index Kp over time.

        **Purpose of the plot:** To monitor global geomagnetic activity and identify periods 
        of geomagnetic storms. The Kp index is a key indicator of the state of Earth's magnetosphere and allows 
        for assessing the intensity of geomagnetic disturbances across the planet.

        **Variables:**
        - **Observation date**: Time of Kp index measurement
        - **Kp Index**: Planetary geomagnetic index on a scale from 0 to 9

        **Kp Scale:**
        - **0-1**: Quiet conditions
        - **2-4**: Unsettled conditions
        - **5**: Geomagnetic storm
        - **6**: Moderate storm
        - **7-9**: Strong to extreme geomagnetic storm
        ''')
    if tcol and ycol:
        fig = px.line(df_p.sort_values(tcol), x=tcol, y=ycol, labels={tcol: "Observation date", ycol: "Kp Index"}, markers=True)
        fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.5))
        set_layout(fig, "Planetary Kp — KpIndex vs Observation date", tcol_data=df_p[tcol],
                    autorange=False)
        add_gray_areas_empty(fig, df_p, tcol)

        y_max = df_p[ycol].max()
        fig.update_yaxes(
            range=[0, y_max + 1]
        )

        st.plotly_chart(fig, width='stretch')
        download_df = df_p[[tcol, ycol]].copy() if tcol and ycol else df_p.copy()
        add_download_button(download_df, "planetary_kp", "Download chart data as CSV")

        df_p['_date'] = pd.to_datetime(df_p[tcol])
        df_p['date'] = df_p['_date'].dt.date
        df_p['hour'] = df_p['_date'].dt.hour
        pivot = df_p.groupby(['date','hour'])[ycol].mean().reset_index()
        heat = pivot.pivot(index='date', columns='hour', values=ycol)
        # ensure hour columns are integers 0-23
        try:
            heat.columns = heat.columns.astype(int)
        except Exception:
            pass
        hours = list(range(24))
        heat = heat.reindex(columns=hours, fill_value=0)
        # sort dates descending
        heat = heat.sort_index(ascending=False).fillna(0)
        st.markdown('#### Heatmap — Kp Index Intensity')
        with st.expander('Description'):
            st.markdown('''
            **Description:** A heatmap showing the average Kp index values grouped 
            by day and UTC hour. Color intensity corresponds to the Kp index value.

            **Purpose of the plot:** To identify temporal patterns of geomagnetic activity and analyze 
            seasonal and daily changes. The visualization allows for quick identification of days and hours 
            with the highest geomagnetic activity.

            **Variables:**
            - **Hour UTC**: Measurement hour in the 0-23 range
            - **Date**: Observation date
            - **Kp Index**: Average planetary geomagnetic index value for a given hour and day
            - **Color Intensity**: Visual representation of the Kp value (red = higher Kp, blue = lower Kp)

            **Interpretation:** Red areas indicate periods of increased geomagnetic activity, 
            while blue areas represent quieter conditions.
            ''')
        x_hours = [f"{int(h):02d}:00" for h in heat.columns]
        def _fmt_date(d):
            try:
                return d.isoformat()
            except Exception:
                return str(d)

        y_dates = [_fmt_date(d) for d in heat.index]
        fig2 = px.imshow(heat.values, x=x_hours, y=y_dates, color_continuous_scale='RdYlBu_r', aspect='auto', labels=dict(x='Hour UTC', y='Date', color='Kp Index'))
        fig2.update_xaxes(tickmode='array')
        fig2.update_yaxes(tickmode='array')
        set_layout(fig2, 'Heatmap Kp (Day vs Hour)', rangeslider=False, legend_title_text="Kp Index values")
        st.plotly_chart(fig2, width='stretch', key='kp_heatmap')
        download_df = pivot.copy()
        add_download_button(download_df, "kp_heatmap", "Download chart data as CSV")

        storms = df_p[df_p[ycol] >= 5]
        if not storms.empty:
            st.markdown('#### Geomagnetic storm analysis')
            with st.expander('Description'):
                st.markdown('''
                **Description:** A scatter plot showing all geomagnetic storm events (Kp ≥ 5) during the analyzed time period.
                
                **Purpose of the plot:** To identify and analyze the occurrence of geomagnetic storms and assess their intensity. The visualization allows for the frequency and temporal distribution of storms, which is important for understanding the cyclical nature of geomagnetic activity.
                
                **Variables:**
                - **Observation date**: Time of geomagnetic storm occurrence
                - **Kp Index**: Kp index value during the storm (always ≥ 5)
                - **Point Color**: Corresponds to the Kp value according to the 'inferno' color palette
                
                **Storm Classification:**
                - **Kp = 5**: Weak storm
                - **Kp = 6**: Moderate storm
                - **Kp = 7**: Strong storm
                - **Kp = 8-9**: Very strong to extreme storm
                ''')
            fig3 = px.scatter(storms, x=tcol, y=ycol, color=ycol, color_continuous_scale='inferno',
                              size=ycol, size_max=12, labels={tcol: 'Observation date', ycol: 'Kp Index', 'estimated_kp': 'Estimated Kp Index'},
                              hover_data={
                                tcol: True,
                                ycol: True,
                                'estimated_kp': True
                            })
            set_layout(fig3, 'Geomagnetic storms points (Kp>=5)', legend_title_text="Kp Index values", tcol_data=df_p[tcol])
            st.plotly_chart(fig3, width='stretch')
            download_df = storms[[tcol, ycol]].copy() if tcol and ycol else storms.copy()
            add_download_button(download_df, "geomagnetic_storms", "Download chart data as CSV")
        else:
            st.write(df_p.head())

    b_table = find_table_like(["boulder"]) or find_table_like(["boulder", "k"]) or find_table_like(["boulder","kindex"])
    logger.debug(f"Found Boulder K table: {b_table}")
    df_b = _load_table_cached(b_table, limit) if b_table else pd.DataFrame()
    if not df_b.empty:
        tcol = pick_time_column(df_b)
        ycol = None
        for c in df_b.columns:
            if c in ("kindex", "k_index", "k"):
                ycol = c
                break
        if not ycol:
            nums = df_b.select_dtypes("number").columns.tolist()
            ycol = nums[0] if nums else None
        st.markdown("#### Boulder K-index — Time Series")
        with st.expander('Description'):
            st.markdown('''
            **Description:** A line chart showing the changes in the local K index measured at the 
            Boulder (USA) observatory over time.

            **Purpose of the plot:** Local assessment of geomagnetic activity in the Boulder region, which may 
            differ from the global planetary Kp index. The local K index is useful for analyzing regional 
            effects of geomagnetic activity and can be more sensitive to local disturbances.

            **Variables:**
            - **Observation date**: Time of K index measurement
            - **K Index**: Local geomagnetic index on a scale from 0 to 9 (measured in Boulder)

            **Interpretation:** Similar to Kp, K values from 0-1 indicate quiet conditions, while 
            values ≥ 5 indicate a geomagnetic storm. The local K index can show regional 
            differences in geomagnetic activity.
            ''')
        if tcol and ycol:
            fig = px.line(df_b.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Observation date', ycol: 'K Index'}, line_shape='spline')
            fig.update_traces(marker=dict(size=3), line=dict(width=1.25))
            set_layout(fig, 'K Index vs Observation date', tcol_data=df_p[tcol])
            add_gray_areas_empty(fig, df_b, tcol)
            st.plotly_chart(fig, width='stretch')
            download_df = df_b[[tcol, ycol]].copy() if tcol and ycol else df_b.copy()
            add_download_button(download_df, "boulder_k_index", "Download chart data as CSV")
        else:
            st.write(df_b.head())