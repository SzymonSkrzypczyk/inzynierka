from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure
import streamlit as st
from babel.dates import format_datetime
import logging

logger = logging.getLogger(__name__)


def set_layout(fig: go.Figure,
               title: str = None,
               rangeslider: bool = True,
               yaxis_title: str = None,
               legend_title_text: str = None,
               tcol_data: pd.Series | None = None,
               autorange: bool = True,
               x_limit_min: pd.Timestamp | None = None,
               x_limit_max: pd.Timestamp | None = None
               ) -> go.Figure:
    """
    Set standard layout for plotly figure

    :param fig:
    :type fig: go.Figure
    :param title:
    :type title: str
    :param yaxis_title:
    :type yaxis_title: str
    :param legend_title_text:
    :type legend_title_text: str
    :param rangeslider:
    :type rangeslider: bool
    :param tcol_data:
    :type tcol_data: pd.Series | None
    :param autorange:
    :type autorange: bool
    :param x_limit_min:
    :type x_limit_min: pd.Timestamp | None
    :param x_limit_max:
    :type x_limit_max: pd.Timestamp | None
    :return:
    """
    logger.debug(f"Setting layout for figure: title={title}, rangeslider={rangeslider}")
    fig.update_layout(template='plotly_white', title={'text': title or '', 'x':0.01},
                      font=dict(family='DejaVu Sans, Arial', size=12),
                      margin=dict(l=40, r=20, t=60, b=40),
                      hovermode='x unified',
                      hoverlabel=dict(bgcolor="white", font_size=12))

    fig.update_yaxes(autorange=autorange)

    if x_limit_min is not None or x_limit_max is not None:
        fig.update_xaxes(range=[x_limit_min, x_limit_max])

    if yaxis_title:
        fig.update_yaxes(title_text=yaxis_title)

    if legend_title_text:
        fig.update_layout(legend_title_text=legend_title_text)

    # formatting dates to use Polish locale
    if tcol_data is not None:
        t = pd.to_datetime(tcol_data).dropna()
        if not t.empty:
            tmin = t.min()
            tmax = t.max()
            logger.debug(f"Formatting dates in Polish locale: range {tmin} to {tmax}")
            
            if rangeslider:
                full_min = tmin - pd.Timedelta(days=1)
                full_max = tmax + pd.Timedelta(days=1)

                fig.update_xaxes(
                    type="date",
                    range=[full_min, full_max],
                    rangeselector=dict(
                        buttons=[
                            dict(
                                count=1,
                                label="1d",
                                step="day",
                                stepmode="backward"
                            ),
                            dict(
                                count=7,
                                label="7d",
                                step="day",
                                stepmode="backward"
                            ),
                            dict(
                                count=1,
                                label="1m",
                                step="month",
                                stepmode="backward"
                            ),
                            dict(
                                label="całość",
                                step="all"
                            ),
                        ]
                    ),
                    rangeslider=dict(visible=True),
                )
                try:
                    num_ticks = 8
                    tick_vals = pd.date_range(start=tmin, end=tmax, periods=num_ticks)
                    tick_texts = [format_datetime(dt.to_pydatetime(), "d MMM yyyy", locale="pl") 
                                 for dt in tick_vals]
                    
                    fig.update_xaxes(
                        tickvals=tick_vals,
                        ticktext=tick_texts,
                        tickmode='array'
                    )
                except Exception:
                    pass
            else:
                try:
                    num_ticks = 8
                    tick_vals = pd.date_range(start=tmin, end=tmax, periods=num_ticks)
                    tick_texts = [format_datetime(dt.to_pydatetime(), "d MMM yyyy", locale="pl") 
                                 for dt in tick_vals]
                    
                    fig.update_xaxes(
                        type="date",
                        tickvals=tick_vals,
                        ticktext=tick_texts,
                        tickmode='array'
                    )
                except Exception:
                    fig.update_xaxes(type="date")

    return fig


def add_gray_areas_empty(fig: Figure, df: pd.DataFrame, tcol: str):
    """
    Add gray areas to the plotly figure for time gaps in the data

    :param fig:
    :type fig: Figure
    :param df:
    :type df: pd.DataFrame
    :param tcol:
    :type tcol: str
    :return:
    """
    try:
        times = pd.to_datetime(df[tcol]).dropna().sort_values().reset_index(drop=True)
        gap_intervals = []
        if len(times) >= 2:
            prev = times.iloc[0]
            for curr in times.iloc[1:]:
                delta = curr - prev
                if delta > pd.Timedelta(days=1):
                    start = prev + pd.Timedelta(seconds=1)
                    end = curr - pd.Timedelta(seconds=1)
                    gap_intervals.append((start, end))
                prev = curr
        if gap_intervals:
            logger.debug(f"Adding {len(gap_intervals)} gray areas for time gaps")
        for start, end in gap_intervals:
            fig.add_vrect(x0=start, x1=end, fillcolor='lightgrey', opacity=0.6, layer='below', line_width=0)
    except Exception as e:
        logger.warning(f"Failed to add gray areas for time gaps: {e}")


def add_download_button(df: pd.DataFrame, filename: str, button_label: str = "Pobierz dane jako CSV"):
    """
    Add a download button for DataFrame data as CSV
    
    :param df: DataFrame to download
    :type df: pd.DataFrame
    :param filename: Base filename (without extension)
    :type filename: str
    :param button_label: Label for the download button
    :type button_label: str
    :return:
    """
    if df is None or df.empty:
        logger.warning(f"Skipping download button for {filename} - DataFrame is empty")
        return

    logger.debug(f"Creating download button for {filename} ({len(df)} rows)")
    csv = df.to_csv(index=False)
    full_filename = f"{filename}.csv"

    st.download_button(
        label=button_label,
        data=csv,
        file_name=full_filename,
        mime="text/csv",
        key=f"download_{filename}_{datetime.now().timestamp()}",
        help="Kliknij, aby pobrać dane w formacie CSV użyte na wykresie.",
        use_container_width=True
    )
