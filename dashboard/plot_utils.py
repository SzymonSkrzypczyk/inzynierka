import plotly.graph_objects as go


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

