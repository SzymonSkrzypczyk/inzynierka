from os import environ
from pathlib import Path
from configparser import ConfigParser

from dotenv import load_dotenv
from retrieval import get_cme, get_gs, get_sf, get_cmea

# target directories
DATA_DIRECTORY = Path(__file__).parent / "data"
CME_DIR = DATA_DIRECTORY / "coronal_mass_ejection"
CMEA_DIR = DATA_DIRECTORY / "coronal_mass_ejection_analysis"
GS_DIR = DATA_DIRECTORY / "geomagnetic_storm"
SF_DIR = DATA_DIRECTORY / "solar_flare"

# create directories if they do not exist
DATA_DIRECTORY.mkdir(exist_ok=True)
CME_DIR.mkdir(exist_ok=True)
CMEA_DIR.mkdir(exist_ok=True)
GS_DIR.mkdir(exist_ok=True)
SF_DIR.mkdir(exist_ok=True)

# read config
CONFIG_FILE = Path(__file__).parent / "config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)
SELECTED_STATISTICS = config.get("target_statistics", "SELECTED_STATISTICS").strip().splitlines()
FREQUENCIES = config.get("settings", "FREQUENCY")

# load API_KEY stored in .env or environment variable
load_dotenv()
NASA_API_KEY = environ.get("NASA_API_KEY")

if NASA_API_KEY is None:
    raise ValueError("API KEY CANNOT BE EMPTY!") from None


