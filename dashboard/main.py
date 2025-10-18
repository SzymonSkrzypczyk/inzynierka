import streamlit as st
import runpy
from pathlib import Path

st.set_page_config(page_title="Panel geomagnetyczny — Multi", layout="wide")
st.title("Panel geomagnetyczny i słoneczny")
st.sidebar.header("Nawigacja")

BASE = Path(__file__).parent
PAGES = [
    ("Geomagnetyzm", "geomag.py"),
    ("Pole magnetyczne", "magnetic_field.py"),
    ("Protony", "protons.py"),
    ("Promieniowanie X", "xray.py"),
    ("Regiony słoneczne", "solar_regions.py")
]

page_names = [p[0] for p in PAGES]
choice = st.sidebar.selectbox("Wybierz typ analizy", page_names)

max_rows = st.sidebar.number_input("Maksymalna liczba wierszy (0 = bez limitu)", min_value=0, value=10000, step=1000)
limit = int(max_rows) if max_rows > 0 else None

sel_index = page_names.index(choice)
sel_file = PAGES[sel_index][1]
sel_path = BASE / sel_file

if not sel_path.exists():
    st.error(f"Plik strony nie znaleziony: {sel_file}")
else:
    try:
        mod = runpy.run_path(str(sel_path))
        if 'render' in mod and callable(mod['render']):
            mod['render'](limit=limit)
        else:
            st.error('Brak funkcji render(limit=...) w module strony')
    except Exception as e:
        st.exception(e)
