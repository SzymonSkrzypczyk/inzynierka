from shutil import make_archive, rmtree
from pathlib import Path
from typing import Union
from datetime import datetime
import csv
import asyncio
import aiohttp
from url_mapping import NAME2URL
from logger import Logger
from send2dropbox import send_to_dropbox

SAVE_DIR = Path(__file__).parent / "data"
RETRY_SLEEP_TIME = 15
MAX_RETRIES = 3
SAVE_DIR.mkdir(parents=True, exist_ok=True)
DROPBOX_DIR = "/inzynierka"
logger = Logger()

async def retrieve_data(target_name: str, url: str, target_dir: Union[str, Path] = SAVE_DIR):
    """
    Retrieve a data for a specific url

    :param target_name:
    :param url:
    :param target_dir:
    :return:
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Retrieving data from URL {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            retries = 0
            while retries < MAX_RETRIES:
                try:
                    if not response.ok:
                        if response.status == 403:
                            logger.log_error(f"Forbidden: {response.status}")
                            raise Exception(f"Forbidden: {response.status}")
                        elif response.status == 500:
                            logger.log_error(f"Server error: {response.status}")
                            raise Exception(f"Server error: {response.status}")
                        elif response.status == 503:
                            logger.log_error(f"Service unavailable: {response.status}")
                            raise Exception(f"Service unavailable: {response.status}")

                    data = await response.json()

                    if data is None or not data:
                        logger.log_error(f"No data found for the given date range")
                        raise Exception(f"No data found for the given date range")

                    # Preprocess the data as needed
                    has_nested = any(isinstance(item, dict) for item in data)
                    if has_nested:
                        logger.log_warning(f"Data contains nested structures, flattening the data for {target_name}")
                        # Flatten the data if it contains nested structures
                        data = [
                            {**item, **{k: v for k, v in item.items() if isinstance(v, dict)}}
                            for item in data
                        ]


                    # Append the data to a CSV file
                    filename = target_dir / f"{target_name}_{datetime.today().date()}.csv"
                    with open(filename, mode='a', newline='') as file:
                        writer = csv.writer(file)
                        # Write the header only if the file is empty
                        if file.tell() == 0:
                            logger.log(f"Writing header for {target_name} to {filename}")
                            writer.writerow(data[0].keys())
                        for item in data:
                            writer.writerow(item.values())

                    logger.log(f"Data retrieved and saved to {filename}")
                except Exception as e:
                    retries += 1
                    logger.log_error(f"Error retrieving data from {url}: {e}. Retrying {retries}/3")
                    logger.log(f"Sleeping for {RETRY_SLEEP_TIME} seconds before retrying")
                    await asyncio.sleep(RETRY_SLEEP_TIME)
            else:
                logger.log_error(f"Failed to retrieve data from {url} after 3 retries")
                raise Exception(f"Failed to retrieve data from {url} after 3 retries")


def compress_data(target_name: str, target_dir: Union[str, Path] = SAVE_DIR, remove_dir: bool = True):
    """
    Compress the data directory into a zip file

    :param target_name:
    :param target_dir:
    :param remove_dir:
    :return:
    """
    target_dir = Path(target_dir)
    target_dir.mkdir(parents=True, exist_ok=True)
    logger.log(f"Compressing data for {target_name}")
    make_archive(
        base_name=str(target_dir.parent / target_name),
        format='zip',
        root_dir=target_dir.parent,
        base_dir=target_dir.name
    )

    if remove_dir:
        logger.log(f"Removing directory {target_dir}")
        rmtree(target_dir, ignore_errors=False)
        logger.log(f"Directory {target_dir} removed")

async def retrieve_all_data():
    """
    Retrieve all data from the URLs in NAME2URL
    """
    tasks = []
    target_dir = SAVE_DIR / f"{datetime.today().date()}"
    for target_name, url in NAME2URL.items():
        tasks.append(retrieve_data(target_name, url, target_dir))
    await asyncio.gather(*tasks)
    logger.log(f"All data retrieved and saved to {target_dir}")
    compress_data(target_dir.name, target_dir)
    logger.log(f"Data compressed to {target_dir}.zip")
    send_to_dropbox(target_dir.parent / f"{target_dir.name}.zip", f"{DROPBOX_DIR}/{target_dir.name}.zip", logger)


if __name__ == "__main__":
    asyncio.run(retrieve_all_data())
