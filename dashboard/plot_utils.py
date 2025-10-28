import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objects import Figure


def set_layout(fig: go.Figure, title: str = None, rangeslider: bool = True):
    fig.update_layout(template='plotly_white', title={'text': title or '', 'x':0.01},
                      font=dict(family='DejaVu Sans, Arial', size=12),
                      margin=dict(l=40, r=20, t=60, b=40),
                      hovermode='x unified')
    if rangeslider:
        fig.update_layout(xaxis=dict(rangeselector=dict(buttons=[
            dict(count=1, label='1d', step='day', stepmode='backward'),
            dict(count=7, label='7d', step='day', stepmode='backward'),
            dict(step='all')
        ]), rangeslider=dict(visible=True), type='date'))
    return fig


def add_gray_areas_empty(fig: Figure, df: pd.DataFrame, tcol: str):
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
