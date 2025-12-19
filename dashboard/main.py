import streamlit as st
import runpy
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

st.set_page_config(page_title="Pogoda kosmiczna", layout="wide")
st.title("Dashboard do analizy pogody kosmicznej")
st.sidebar.header("Opcje")

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

sel_index = page_names.index(choice)
sel_file = PAGES[sel_index][1]
sel_path = BASE / sel_file

logger.info(f"User selected page: {choice} ({sel_file})")

if not sel_path.exists():
    logger.error(f"Page file not found: {sel_file}")
    st.error(f"Plik strony nie znaleziony: {sel_file}")
else:
    try:
        logger.info(f"Loading and rendering page: {sel_file}")
        mod = runpy.run_path(str(sel_path))
        if 'render' in mod and callable(mod['render']):
            mod['render']()
            logger.info(f"Successfully rendered page: {sel_file}")
        else:
            logger.error(f"Page {sel_file} does not have a render() function")
            st.error('Brak funkcji render(limit=...) w module strony')
    except Exception as e:
        logger.exception(f"Error rendering page {sel_file}: {e}")
        st.exception(e)
