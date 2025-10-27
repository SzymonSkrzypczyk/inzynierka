import streamlit as st
import plotly.express as px
import pandas as pd

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column
from plot_utils import set_layout, add_gray_areas_empty


def _classify_flux(v):
    try:
        v = float(v)
    except Exception:
        return 'Unknown'
    if v <= 0:
        return 'Unknown'
    if v >= 1e-4:
        return 'X'
    if v >= 1e-5:
        return 'M'
    if v >= 1e-6:
        return 'C'
    return 'A/B'


@st.cache_data(ttl=600)
def _load_table_cached(name, limit):
    return read_table(name, limit=limit)


def render(limit=None):
    st.title('Promieniowanie rentgenowskie Słońca')
    p_tab = find_table_like(['primary','xray'])
    s_tab = find_table_like(['secondary','xray'])
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Primary', df_p), ('Secondary', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} X-ray')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Strumienie promieniowania X według satelity')
        with st.expander('Opis'):
            st.markdown('''
            **Promieniowanie rentgenowskie Słońca** jest emitowane podczas rozbłysków słonecznych 
            i aktywności koronalnej. Wykres pokazuje strumienie promieniowania X w różnych 
            pasmach energetycznych (Primary: 0.5-4 Å, Secondary: 1-8 Å) mierzone przez różne 
            satelity. Nagłe wzrosty strumienia wskazują na rozbłyski słoneczne klasy C, M lub X.
            ''')
        if 'satellite' in df.columns and 'flux' in df.columns:
            fig = px.line(df.sort_values(tcol), x=tcol, y='flux', color='satellite', labels={tcol:'Czas','flux':'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.6))
            set_layout(fig, f'{name} — Strumienie promieniowania X według satelity')
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol:'Czas', ycol:'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=['#636EFA'])
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.4))
            set_layout(fig, f'{name} — Strumienie promieniowania X')


        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, use_container_width=True)

        if 'flux' in df.columns:
            st.subheader('Klasyfikacja rozbłysków słonecznych')
            with st.expander('Opis'):
                st.markdown('''
                **Klasyfikacja rozbłysków** według intensywności promieniowania X:
                - **Klasa A/B**: < 10⁻⁶ W·m⁻² (bardzo słabe)
                - **Klasa C**: 10⁻⁶ - 10⁻⁵ W·m⁻² (słabe)
                - **Klasa M**: 10⁻⁵ - 10⁻⁴ W·m⁻² (umiarkowane)
                - **Klasa X**: ≥ 10⁻⁴ W·m⁻² (silne)
                
                Silne rozbłyski klasy X mogą powodować zakłócenia w komunikacji radiowej, 
                systemach nawigacyjnych i sieciach energetycznych.
                ''')
            df['flare_class'] = df['flux'].apply(_classify_flux)
            fig2 = px.scatter(df, x=tcol, y='flux', color='flare_class', labels={tcol:'Czas','flux':'Strumień [W·m⁻²]'}, log_y=True,
                              color_discrete_map={'X':'#7f0000','M':'#ff7f0e','C':'#1f77b4','A/B':'#8c564b','Unknown':'#d3d3d3'})
            fig2.update_traces(marker=dict(size=6))
            set_layout(fig2, f'{name} — Klasyfikacja rozbłysków słonecznych')
            add_gray_areas_empty(fig2, df, tcol)
            st.plotly_chart(fig2, use_container_width=True)

        pk_tab = find_table_like(['planetary','kp']) or find_table_like(['kp','index'])
        df_k = _load_table_cached(pk_tab, limit) if pk_tab else pd.DataFrame()
        if not df_k.empty:
            kcol = None
            for c in df_k.columns:
                if c in ('kpindex','kp_index','kp') or c.endswith('kp'):
                    kcol = c
                    break
            if kcol is None:
                numcols = df_k.select_dtypes('number').columns
                kcol = numcols[0] if len(numcols)>0 else None
            if kcol:
                df['date'] = pd.to_datetime(df[tcol]).dt.date
                df_k['date'] = pd.to_datetime(df_k[pick_time_column(df_k)]).dt.date
                mean_k = df_k.groupby('date')[kcol].mean().reset_index()
                merged = df.merge(mean_k, on='date', how='left')
                st.subheader('Korelacja rozbłysków z aktywnością geomagnetyczną')
                fig3 = px.scatter(merged, x='flux', y=kcol, labels={'flux': 'Strumień [W·m⁻²]', kcol: 'Indeks Kp'},
                                  color_discrete_sequence=['#636EFA'])
                set_layout(fig3, 'Korelacja rozbłysków słonecznych z aktywnością geomagnetyczną')
                st.plotly_chart(fig3, use_container_width=True)

        st.subheader('Rozkład statystyczny strumieni promieniowania X')
        with st.expander('Opis'):
            st.markdown('''
            **Histogram strumieni** pokazuje rozkład wartości promieniowania rentgenowskiego 
            w wybranym przedziale czasowym. Większość czasu Słońce emituje niskie strumienie 
            (klasa A/B), podczas gdy silne rozbłyski (klasa X) są rzadkie ale intensywne. 
            Analiza rozkładu pozwala ocenić ogólną aktywność słoneczną w danym okresie.
            ''')
        fig4 = px.histogram(df, x='flux', nbins=80, labels={'flux':'Strumień [W·m⁻²]'}, log_y=True, color_discrete_sequence=['#00CC96'])
        set_layout(fig4, 'Rozkład statystyczny strumieni promieniowania X', rangeslider=False)
        st.plotly_chart(fig4, use_container_width=True)
