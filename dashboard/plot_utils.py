import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure


def set_layout(fig: go.Figure,
               title: str = None,
               rangeslider: bool = True,
               yaxis_title: str = None,
               legend_title_text: str = None
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
    :return:
    """
    fig.update_layout(template='plotly_white', title={'text': title or '', 'x':0.01},
                      font=dict(family='DejaVu Sans, Arial', size=12),
                      margin=dict(l=40, r=20, t=60, b=40),
                      hovermode='x unified')
    if yaxis_title:
        fig.update_yaxes(title_text=yaxis_title)

    if legend_title_text:
        fig.update_layout(legend_title_text=legend_title_text)

    if rangeslider:
        fig.update_layout(xaxis=dict(rangeselector=dict(buttons=[
            dict(count=1, label='1d', step='day', stepmode='backward'),
            dict(count=7, label='7d', step='day', stepmode='backward'),
            dict(step='all')
        ]), rangeslider=dict(visible=True), type='date'))
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
        for start, end in gap_intervals:
            fig.add_vrect(x0=start, x1=end, fillcolor='lightgrey', opacity=0.6, layer='below', line_width=0)
    except Exception:
        pass
