"""Behavior tests for the interplanetary magnetic-field dashboard page."""

import importlib.util
import sys
from contextlib import nullcontext
from pathlib import Path
from types import SimpleNamespace

import pandas as pd


class FakeStreamlit:
    def __init__(self):
        self.titles = []
        self.charts = []

    def cache_data(self, **_kwargs):
        return lambda func: func

    def title(self, value):
        self.titles.append(value)

    def subheader(self, _value):
        pass

    def expander(self, _value):
        return nullcontext()

    def markdown(self, _value):
        pass

    def plotly_chart(self, figure, **_kwargs):
        self.charts.append(figure)

    def info(self, _value):
        pass


def load_page(fake_streamlit):
    dashboard_dir = Path(__file__).parent
    sys.path.insert(0, str(dashboard_dir))
    sys.modules["streamlit"] = fake_streamlit
    spec = importlib.util.spec_from_file_location(
        "magnetic_field_under_test", dashboard_dir / "magnetic_field.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_render_shows_interplanetary_magnetic_field_charts(monkeypatch):
    fake_streamlit = FakeStreamlit()
    module = load_page(fake_streamlit)
    frame = pd.DataFrame(
        {
            "time_tag": pd.to_datetime(["2026-09-02T13:35:00"]),
            "bt": [5.63],
            "bx_gsm": [5.22],
            "by_gsm": [-1.03],
            "bz_gsm": [1.84],
        }
    )
    monkeypatch.setattr(module, "find_table_like", lambda _keywords: "dscovr_mag1s")
    monkeypatch.setattr(module, "_load_table_cached", lambda _name, _limit: frame)
    monkeypatch.setattr(module, "add_download_button", lambda *_args: None)

    module.render()

    assert fake_streamlit.titles == ["Interplanetary Magnetic Field"]
    assert len(fake_streamlit.charts) == 2
    assert fake_streamlit.charts[0].layout.title.text == "Interplanetary Magnetic Field Components"
