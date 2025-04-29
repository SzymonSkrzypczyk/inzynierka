from os import environ
from pathlib import Path
from configparser import ConfigParser
import asyncio

from dotenv import load_dotenv
from retrieval import get_cme, get_gs, get_sf, get_cmea
from save_to_csv import save_to_csv

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


async def retrieve_data():
    """
    Load data that has

    :return:
    """
    tasks = {}

    if "coronal_mass_ejection" in SELECTED_STATISTICS:
        tasks["coronal_mass_ejection"] = get_cme(api_key=NASA_API_KEY)

    if "coronal_mass_ejection_analysis" in SELECTED_STATISTICS:
        tasks["coronal_mass_ejection_analysis"] = get_cmea(api_key=NASA_API_KEY)

    if "geomagnetic_storm" in SELECTED_STATISTICS:
        tasks["geomagnetic_storm"] = get_gs(api_key=NASA_API_KEY)

    if "solar_flare" in SELECTED_STATISTICS:
        tasks["solar_flare"] = get_sf(api_key=NASA_API_KEY)

    results = await asyncio.gather(*tasks.values())
    return dict(zip(tasks.keys(), results))


def process_data(
        data: dict,
        target_directory: Path
):
    """
    Process data and save to csv

    :param data:
    :param target_directory:
    :return:
    """
    for key, value in data.items():
        item_target_directory = target_directory / key
        if value:
            save_to_csv(
                target_name=key,
                target_directory=item_target_directory,
                data=value
            )


def main():
    """
    Main execution function to retrieve and save data

    :return:
    """
    results = asyncio.run(retrieve_data())
    process_data(results, DATA_DIRECTORY)
    print("Data retrieval and saving completed.")


if __name__ == '__main__':
    main()
