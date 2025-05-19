from pathlib import Path
from datetime import datetime
import csv
import asyncio
import aiohttp
from url_mapping import NAME2URL

SAVE_DIR = Path(__file__).parent / "data"
SAVE_DIR.mkdir(parents=True, exist_ok=True)


async def retrieve_data(target_name: str, url: str):
    """
    Retrieve a data for a specific url

    :param target_name:
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if not response.ok:
                if response.status == 403:
                    raise Exception(f"Forbidden: {response.status}")
                elif response.status == 500:
                    raise Exception(f"Server error: {response.status}")
                elif response.status == 503:
                    raise Exception(f"Service unavailable: {response.status}")

            data = await response.json()

            if data is None or not data:
                raise Exception(f"No data found for the given date range")

            # Preprocess the data as needed
            has_nested = any(isinstance(item, dict) for item in data)
            if has_nested:
                # Flatten the data if it contains nested structures
                data = [
                    {**item, **{k: v for k, v in item.items() if isinstance(v, dict)}}
                    for item in data
                ]


            # Append the data to a CSV file
            filename = SAVE_DIR / f"{target_name}_{datetime.today().date()}.csv"
            with open(filename, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write the header only if the file is empty
                if file.tell() == 0:
                    writer.writerow(data[0].keys())
                for item in data:
                    writer.writerow(item.values())


async def retrieve_all_data():
    """
    Retrieve all data from the URLs in NAME2URL
    """
    tasks = []
    for target_name, url in NAME2URL.items():
        tasks.append(retrieve_data(target_name, url))
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(retrieve_all_data())
