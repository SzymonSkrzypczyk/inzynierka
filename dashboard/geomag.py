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
        st.markdown("#### Planetarny Kp — wykres czasowy")
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres liniowy przedstawia zmiany planetarnego indeksu geomagnetycznego Kp w czasie.
            
            **Cel wykresu:** Monitorowanie globalnej aktywności geomagnetycznej i identyfikacja okresów 
            burz geomagnetycznych. Indeks Kp jest kluczowym wskaźnikiem stanu magnetosfery Ziemi i pozwala 
            ocenić intensywność zakłóceń geomagnetycznych na całej planecie.
            
            **Zmienne:**
            - **Czas**: Moment pomiaru indeksu Kp
            - **Indeks Kp**: Planetarny indeks geomagnetyczny w skali od 0 do 9
            
            **Skala Kp:**
            - **0-1**: Spokojne warunki
            - **2-4**: Niespokojne warunki
            - **5**: Burza geomagnetyczna
            - **6**: Burza umiarkowana
            - **7-9**: Silna do ekstremalnej burza geomagnetyczna
            ''')
        if tcol and ycol:
            fig = px.line(df_p.sort_values(tcol), x=tcol, y=ycol, labels={tcol: "Czas", ycol: "Indeks Kp"}, markers=True)
            fig.update_traces(mode='lines+markers', marker=dict(size=4), line=dict(width=1.5))
            _set_layout(fig, "Planetarny Kp — KpIndex vs Czas")
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
            st.markdown('#### Heatmap — intensywność KpIndex')
            with st.expander('Opis'):
                st.markdown('''
                **Opis:** Mapa cieplna przedstawiająca średnie wartości indeksu Kp pogrupowane 
                według dnia i godziny UTC. Intensywność koloru odpowiada wartości indeksu Kp.
                
                **Cel wykresu:** Identyfikacja wzorców czasowych aktywności geomagnetycznej oraz analiza 
                sezonowych i dobowych zmian. Wizualizacja pozwala szybko zidentyfikować dni i godziny 
                o największej aktywności geomagnetycznej.
                
                **Zmienne:**
                - **Godzina UTC**: Godzina pomiaru w zakresie 0-23
                - **Data**: Data obserwacji
                - **Indeks Kp**: Średnia wartość planetarnego indeksu geomagnetycznego dla danej godziny i dnia
                - **Intensywność koloru**: Wizualna reprezentacja wartości Kp (czerwony = wyższy Kp, niebieski = niższy Kp)
                
                **Interpretacja:** Czerwone obszary wskazują okresy zwiększonej aktywności geomagnetycznej, 
                podczas gdy niebieskie obszary reprezentują spokojniejsze warunki.
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
            _set_layout(fig2, 'Heatmap Kp (dzień vs godzina)', rangeslider=False)
            st.plotly_chart(fig2, use_container_width=True)

            storms = df_p[df_p[ycol] >= 5]
            if not storms.empty:
                st.markdown('#### Analiza burz geomagnetycznych')
                with st.expander('Opis'):
                    st.markdown('''
                    **Opis:** Wykres punktowy przedstawiający wszystkie momenty, w których wystąpiły burze 
                    geomagnetyczne (Kp ≥ 5) w analizowanym okresie czasowym.
                    
                    **Cel wykresu:** Identyfikacja i analiza występowania burz geomagnetycznych oraz ocena 
                    ich intensywności. Wizualizacja pozwala zobaczyć częstotliwość i rozkład czasowy burz, 
                    co jest istotne dla zrozumienia cykliczności aktywności geomagnetycznej.
                    
                    **Zmienne:**
                    - **Czas**: Moment wystąpienia burzy geomagnetycznej
                    - **Kp**: Wartość indeksu Kp podczas burzy (zawsze ≥ 5)
                    - **Kolor punktu**: Odpowiada wartości Kp zgodnie z paletą kolorów 'inferno'
                    
                    **Klasyfikacja burz:**
                    - **Kp = 5**: Burza słaba
                    - **Kp = 6**: Burza umiarkowana
                    - **Kp = 7**: Burza silna
                    - **Kp = 8-9**: Burza bardzo silna do ekstremalnej
                    ''')
                fig3 = px.scatter(storms, x=tcol, y=ycol, color=ycol, color_continuous_scale='inferno',
                                  size=ycol, size_max=12, labels={tcol: 'Czas', ycol: 'Kp'}, hover_data=storms.columns)
                _set_layout(fig3, 'Punkty burz geomagnetycznych (Kp>=5)')
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
        st.markdown("#### Boulder K-index — wykres czasowy")
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres liniowy przedstawiający zmiany lokalnego indeksu K mierzonego w obserwatorium 
            Boulder (USA) w czasie.
            
            **Cel wykresu:** Lokalna ocena aktywności geomagnetycznej w regionie Boulder, która może różnić 
            się od globalnego indeksu planetarnego Kp. Indeks lokalny K jest przydatny do analizy regionalnych 
            efektów aktywności geomagnetycznej i może być bardziej wrażliwy na lokalne zakłócenia.
            
            **Zmienne:**
            - **Czas**: Moment pomiaru indeksu K
            - **Indeks K**: Lokalny indeks geomagnetyczny w skali od 0 do 9 (mierzony w Boulder)
            
            **Interpretacja:** Podobnie jak Kp, wartości K od 0-1 oznaczają spokojne warunki, podczas gdy 
            wartości ≥ 5 wskazują na burzę geomagnetyczną. Lokalny indeks K może pokazywać różnice 
            regionalne w aktywności geomagnetycznej.
            ''')
        if tcol and ycol:
            fig = px.line(df_b.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Czas', ycol: 'Indeks K'}, line_shape='spline')
            fig.update_traces(marker=dict(size=3), line=dict(width=1.25))
            _set_layout(fig, 'Index K vs Czas')
            add_gray_areas_empty(fig, df_b, tcol)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write(df_b.head())