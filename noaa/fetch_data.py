from pathlib import Path
from typing import Union
from datetime import datetime
import csv
import asyncio
import aiohttp
from url_mapping import NAME2URL
from logger import Logger

SAVE_DIR = Path(__file__).parent / "data"
SAVE_DIR.mkdir(parents=True, exist_ok=True)
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

async def retrieve_all_data():
    """
    Retrieve all data from the URLs in NAME2URL
    """
    tasks = []
    target_dir = SAVE_DIR / f"{datetime.today().date()}"
    for target_name, url in NAME2URL.items():
        tasks.append(retrieve_data(target_name, url, target_dir))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(retrieve_all_data())
