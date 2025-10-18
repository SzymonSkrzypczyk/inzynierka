import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column


def _set_layout(fig: go.Figure, title: str = None, rangeslider: bool = True):
    fig.update_layout(template='plotly_white', title={'text': title, 'x':0.01},
                      font=dict(family='Arial', size=12),
                      margin=dict(l=40, r=20, t=60, b=40),
                      hovermode='x unified')
    # enable rangeslider for time series only when requested
    if rangeslider and 'xaxis' in fig.layout:
        fig.update_layout(xaxis=dict(rangeselector=dict(buttons=[
            dict(count=1, label='1d', step='day', stepmode='backward'),
            dict(count=7, label='7d', step='day', stepmode='backward'),
            dict(step='all')
        ]), rangeslider=dict(visible=True), type='date'))
    return fig


def _detect_k_column(df):
    for c in df.columns:
        if c in ("kpindex", "kp_index", "kp") or c.endswith("kpindex"):
            return c
    nums = df.select_dtypes("number").columns.tolist()
    return nums[0] if nums else None


def render(limit=None):
    st.title("Geomagnetyzm")
    st.subheader("Planetarny i lokalny K-index")

    p_table = find_table_like(["planetary", "k"]) or find_table_like(["k", "index"]) or find_table_like(["planetary","kp"])
    df_p = read_table(p_table, limit=limit) if p_table else pd.DataFrame()
    if not df_p.empty:
        tcol = pick_time_column(df_p)
        ycol = _detect_k_column(df_p)
        st.markdown("#### Planetarny Kp — wykres czasowy")
        with st.expander('Opis'):
            st.markdown('''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
            ''')
        if tcol and ycol:
            fig = px.line(df_p.sort_values(tcol), x=tcol, y=ycol, labels={tcol: "Czas", ycol: "Kp"}, markers=True)
            fig.update_traces(mode='lines+markers', marker=dict(size=4))
            _set_layout(fig, "Planetarny Kp — KpIndex vs Czas")
            st.plotly_chart(fig, use_container_width=True)

            df_p['_date'] = pd.to_datetime(df_p[tcol])
            df_p['date'] = df_p['_date'].dt.date
            df_p['hour'] = df_p['_date'].dt.hour
            pivot = df_p.groupby(['date','hour'])[ycol].mean().reset_index()
            heat = pivot.pivot(index='date', columns='hour', values=ycol)
            # ensure hour columns are integers and include full 0-23 range for consistent plotting
            try:
                heat.columns = heat.columns.astype(int)
            except Exception:
                pass
            hours = list(range(24))
            heat = heat.reindex(columns=hours, fill_value=0)
            # sort dates descending (most recent first)
            heat = heat.sort_index(ascending=False).fillna(0)
            st.markdown('#### Heatmap — intensywność KpIndex (średnia)')
            with st.expander('Opis'):
                st.markdown('''
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
                ''')
            # prepare explicit labels so hours are treated as categorical (not dates)
            x_hours = [f"{int(h):02d}:00" for h in heat.columns]
            # format y axis dates as ISO strings to avoid ambiguous types
            def _fmt_date(d):
                try:
                    return d.isoformat()
                except Exception:
                    return str(d)

            y_dates = [_fmt_date(d) for d in heat.index]
            fig2 = px.imshow(heat.values, x=x_hours, y=y_dates, color_continuous_scale='RdYlBu_r', aspect='auto', labels=dict(x='Godzina', y='Data', color='Kp'))
            fig2.update_xaxes(tickmode='array')
            fig2.update_yaxes(tickmode='array')
            # don't apply date rangeslider to heatmap (columns are categorical hours)
            _set_layout(fig2, 'Heatmap Kp (dzień vs godzina)', rangeslider=False)
            st.plotly_chart(fig2, use_container_width=True)

            # scatter for storms
            storms = df_p[df_p[ycol] >= 5]
            if not storms.empty:
                st.markdown('#### Burze geomagnetyczne — Kp >= 5')
                with st.expander('Opis'):
                    st.markdown('''
                    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
                    ''')
                fig3 = px.scatter(storms, x=tcol, y=ycol, color=ycol, color_continuous_scale='inferno',
                                  size=ycol, size_max=12, labels={tcol: 'Czas', ycol: 'Kp'}, hover_data=storms.columns)
                _set_layout(fig3, 'Punkty burz geomagnetycznych (Kp>=5)')
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.write(df_p.head())

    b_table = find_table_like(["boulder"]) or find_table_like(["boulder", "k"]) or find_table_like(["boulder","kindex"])
    df_b = read_table(b_table, limit=limit) if b_table else pd.DataFrame()
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
        st.markdown("#### Boulder K-index — wykres czasowy")
        with st.expander('Opis'):
            st.markdown('''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas ac sapien accumsan, ornare felis vitae, eleifend erat. Sed ut erat orci. Mauris vehicula nulla sed quam tincidunt, et mattis mauris semper. Nulla tristique lectus id lobortis placerat. Suspendisse potenti. Proin scelerisque, dui ut ullamcorper pulvinar, tellus felis dignissim quam, non vestibulum ligula enim vitae tellus
            ''')
        if tcol and ycol:
            fig = px.line(df_b.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'K-index'}, line_shape='spline')
            fig.update_traces(marker=dict(size=3))
            _set_layout(fig, 'Boulder K-index — KIndex vs Czas')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(df_b.head())