from typing import Optional, Union
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

try:
    from db import find_table_like, read_table, pick_time_column
except Exception:
    from dashboard.db import find_table_like, read_table, pick_time_column

try:
    from plot_utils import set_layout, add_gray_areas_empty
except Exception:
    from dashboard.plot_utils import set_layout, add_gray_areas_empty


def _parse_energy_val(e: Union[str, float, int, None]) -> float:
    """
    Parse energy value from string or number

    :param e:
    :type e: Union[str, float, int, None]
    :return:
    :rtype: float
    """
    if pd.isna(e):
        return np.nan
    if isinstance(e, (int, float)):
        return float(e)
    s = str(e)
    m = ''.join(ch if (ch.isdigit() or ch=='.') else ' ' for ch in s)
    parts = [p for p in m.split() if p]
    return float(parts[0]) if parts else np.nan


@st.cache_data(ttl=600)
def _load_table_cached(name: str, limit: Optional[int] = None):
    """
    Load table with caching

    :param name:
    :type name: str
    :param limit:
    :type limit: Optional[int]
    :return:
    """
    return read_table(name, limit=limit)


def render(limit: Optional[int] = None):
    """
    Render proton radiation (integral fluxes) section

    :param limit:
    :type limit: Optional[int]
    :return:
    """
    st.title('Promieniowanie protonowe — strumienie integralne')
    p_tab = find_table_like(['primary','integral','proton'])
    s_tab = find_table_like(['secondary','integral','proton'])
    df_p = _load_table_cached(p_tab, limit) if p_tab else pd.DataFrame()
    df_s = _load_table_cached(s_tab, limit) if s_tab else pd.DataFrame()

    for name, df in (('Główny źródło danych', df_p), ('Zapasowe źródło danych', df_s)):
        if df.empty:
            st.info(f'Brak danych: {name} Integral Protons')
            continue
        tcol = pick_time_column(df)
        if tcol is None:
            st.write(df.head())
            continue
        st.subheader(f'{name} — Strumienie protonowe według energii')
        with st.expander('Opis'):
            st.markdown('''
            **Opis:** Wykres przedstawia czasowe zmiany strumienia protonów (cząstek naładowanych) 
            pochodzących ze Słońca i przestrzeni kosmicznej w różnych pasmach energetycznych.
            
            **Cel wykresu:** Monitorowanie poziomów promieniowania protonowego, które może stanowić 
            zagrożenie dla astronautów, satelitów i systemów elektronicznych.
            
            **Zmienne:**
            - **Data obserwacji**: Moment pomiaru strumienia protonowego
            - **Strumień [cm⁻²·s⁻¹]**: Liczba protonów przechodzących przez powierzchnię 1 cm² w ciągu sekundy
            - **Energia**: Pasmo energetyczne protonów (jeśli dostępne w danych)
            
            **Interpretacja:**
            - **Protony niskoenergetyczne**: Pochodzą głównie ze Słońca, związane z rozbłyskami słonecznymi
            - **Protony wysokoenergetyczne**: Pochodzą z przestrzeni kosmicznej, mogą powodować zwiększone 
            promieniowanie na wysokościach lotniczych
            - **Nagłe wzrosty strumienia**: Wskazują na rozbłyski słoneczne lub koronalne wyrzuty masy
            ''')
        if 'energy' in df.columns:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, color='energy', labels={tcol: 'Data obserwacji', ycol: 'pfu(particle flux unit)'}, log_y=True, markers=True, color_discrete_sequence=px.colors.qualitative.Dark24)
            fig.update_traces(line=dict(width=2), marker=dict(size=5))
            set_layout(fig, f'{name} — Strumienie protonowe według energii', rangeslider=True, legend_title_text="Energia protonów")
        else:
            ycol = 'flux' if 'flux' in df.columns else df.select_dtypes('number').columns[0]
            fig = px.line(df.sort_values(tcol), x=tcol, y=ycol, labels={tcol: 'Data obserwacji', ycol: 'pfu(particle flux unit)'}, log_y=True, markers=True)
            fig.update_traces(line=dict(width=1.8), marker=dict(size=4))
            set_layout(fig, f'{name} — Strumienie protonowe', rangeslider=True, legend_title_text="Energia protonów")

        add_gray_areas_empty(fig, df, tcol)
        st.plotly_chart(fig, use_container_width=True)
