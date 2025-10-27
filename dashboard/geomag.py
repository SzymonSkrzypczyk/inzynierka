import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column
from plot_utils import add_gray_areas_empty


def _set_layout(fig: go.Figure, title: str = None, rangeslider: bool = True):
    fig.update_layout(template='plotly_white', title={'text': title, 'x':0.01},
                      font=dict(family='Arial', size=12),
                      margin=dict(l=40, r=20, t=60, b=40),
                      hovermode='x unified')
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


@st.cache_data(ttl=600)
def _load_table_cached(name, limit):
    return read_table(name, limit=limit)


def render(limit=None):
    st.title("Geomagnetyzm")
    st.subheader("Planetarny i lokalny K-index")

    p_table = find_table_like(["planetary", "k"]) or find_table_like(["k", "index"]) or find_table_like(["planetary","kp"])
    df_p = _load_table_cached(p_table, limit) if p_table else pd.DataFrame()
    if not df_p.empty:
        tcol = pick_time_column(df_p)
        ycol = _detect_k_column(df_p)
        st.markdown("#### Planetarny indeks Kp — analiza czasowa")
        with st.expander('Opis'):
            st.markdown('''
            **Planetarny indeks geomagnetyczny Kp** przedstawia globalną aktywność geomagnetyczną Ziemi w skali 0-9. 
            Wartości Kp ≥ 5 oznaczają burze geomagnetyczne, które mogą wpływać na systemy nawigacyjne, 
            komunikację radiową i sieci energetyczne. Wykres pozwala monitorować długoterminowe trendy 
            aktywności geomagnetycznej oraz identyfikować okresy zwiększonej aktywności słonecznej.
            ''')
        if tcol and ycol:
            fig = px.line(df_p.sort_values(tcol), x=tcol, y=ycol, labels={tcol: "Czas", ycol: "Indeks Kp"}, markers=True)
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.5))
            _set_layout(fig, "Planetarny indeks geomagnetyczny Kp w czasie")
            add_gray_areas_empty(fig, df_p, tcol)
            st.plotly_chart(fig, use_container_width=True)

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
            st.markdown('#### Mapa cieplna aktywności geomagnetycznej')
            with st.expander('Opis'):
                st.markdown('''
                **Mapa cieplna** przedstawia średnie wartości indeksu Kp w układzie dzień-godzina. 
                Intensywność koloru odpowiada sile aktywności geomagnetycznej - od spokojnych warunków (jasne kolory) 
                do silnych burz geomagnetycznych (ciemne kolory). Wizualizacja pozwala łatwo identyfikować 
                wzorce czasowe aktywności oraz okresy zwiększonej aktywności słonecznej.
                ''')
            x_hours = [f"{int(h):02d}:00" for h in heat.columns]
            def _fmt_date(d):
                try:
                    return d.isoformat()
                except Exception:
                    return str(d)

            y_dates = [_fmt_date(d) for d in heat.index]
            fig2 = px.imshow(heat.values, x=x_hours, y=y_dates, color_continuous_scale='RdYlBu_r', aspect='auto', labels=dict(x='Godzina UTC', y='Data', color='Indeks Kp'))
            fig2.update_xaxes(tickmode='array')
            fig2.update_yaxes(tickmode='array')
            _set_layout(fig2, 'Mapa cieplna aktywności geomagnetycznej (dzień vs godzina)', rangeslider=False)
            st.plotly_chart(fig2, use_container_width=True)

            storms = df_p[df_p[ycol] >= 5]
            if not storms.empty:
                st.markdown('#### Analiza burz geomagnetycznych')
                with st.expander('Opis'):
                    st.markdown('''
                    **Burze geomagnetyczne** to okresy intensywnej aktywności geomagnetycznej (Kp ≥ 5), 
                    wywołane przez wiatr słoneczny i koronalne wyrzuty masy. Silne burze mogą powodować 
                    zakłócenia w systemach nawigacyjnych GPS, komunikacji radiowej, sieciach energetycznych 
                    oraz zwiększać promieniowanie kosmiczne na dużych wysokościach lotów.
                    ''')
                fig3 = px.scatter(storms, x=tcol, y=ycol, color=ycol, color_continuous_scale='inferno',
                                  size=ycol, size_max=12, labels={tcol: 'Czas', ycol: 'Indeks Kp'}, hover_data=storms.columns)
                _set_layout(fig3, 'Epizody burz geomagnetycznych (Kp ≥ 5)')
                st.plotly_chart(fig3, use_container_width=True)
        else:
            st.write(df_p.head())

    b_table = find_table_like(["boulder"]) or find_table_like(["boulder", "k"]) or find_table_like(["boulder","kindex"])
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
        st.markdown("#### Lokalny indeks K (Boulder) — analiza czasowa")
        with st.expander('Opis'):
            st.markdown('''
            **Lokalny indeks K** z obserwatorium Boulder (NOAA) przedstawia aktywność geomagnetyczną 
            w konkretnej lokalizacji geograficznej. W przeciwieństwie do planetarnego indeksu Kp, 
            lokalny indeks K może wykazywać większe wahania i jest bardziej wrażliwy na lokalne 
            warunki geomagnetyczne. Dane te są szczególnie przydatne do analizy regionalnych 
            efektów aktywności słonecznej.
            ''')
        if tcol and ycol:
            fig = px.line(df_b.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Indeks K'}, line_shape='spline')
            fig.update_traces(marker=dict(size=3), line=dict(width=1.25))
            _set_layout(fig, 'Lokalny indeks K (Boulder) w czasie')
            add_gray_areas_empty(fig, df_b, tcol)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(df_b.head())