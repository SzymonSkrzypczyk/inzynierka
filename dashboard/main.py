import streamlit as st
import importlib.util
import sys
from pathlib import Path

st.set_page_config(page_title="Pogoda kosmiczna", layout="wide")
st.title("Dashboard do analizy pogody kosmicznej")
st.sidebar.header("Opcje")

BASE = Path(__file__).parent
PAGES = [
    ("Geomagnetyzm", "geomag.py"),
    ("Pole magnetyczne", "magnetic_field.py"),
    ("Protony", "protons.py"),
    ("Promieniowanie X", "xray.py"),
    ("Regiony słoneczne", "solar_regions.py"),
]

page_names = [p[0] for p in PAGES]
choice = st.sidebar.selectbox("Wybierz typ analizy", page_names)

sel_index = page_names.index(choice)
sel_name, sel_file = PAGES[sel_index]
sel_path = BASE / sel_file

def load_page_module(_module_name: str, path: Path):
    """
    Load a Streamlit page as a real Python module so that
    widgets are tracked correctly and session_state works.
    """
    if _module_name in sys.modules:
        return sys.modules[_module_name]

    spec = importlib.util.spec_from_file_location(_module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[_module_name] = module
    spec.loader.exec_module(module)
    return module

if not sel_path.exists():
    st.error(f"Plik strony nie znaleziony: {sel_file}")
else:
    try:
        module_name = f"page_{sel_index}_{sel_file.replace('.py', '')}"
        page = load_page_module(module_name, sel_path)

        if hasattr(page, "render") and callable(page.render):
            page.render()
        else:
            st.error("Brak funkcji render() w module strony")

    except Exception as e:
        st.exception(e)
