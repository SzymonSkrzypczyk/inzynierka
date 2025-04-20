from typing import Optional
from datetime import date, timedelta
import asyncio
import aiohttp

CME_URL = "https://api.nasa.gov/DONKI/CME"
CMEA_URL = "https://api.nasa.gov/DONKI/CMEAnalysis"
GS_URL = "https://api.nasa.gov/DONKI/GST"
FS_URL = "https://api.nasa.gov/DONKI/FLR"

from dotenv import load_dotenv
from os import environ
load_dotenv()
NASA_API_KEY = environ.get("NASA_API_KEY")


async def get_cme(
        api_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    """
    Retrieve data for coronal mass ejection

    :param api_key:
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date is None:
        start_date = date.today() - timedelta(30)

    if end_date is None:
        end_date = date.today()

    async with aiohttp.ClientSession() as session:
        async with session.get(CME_URL,
                               params={"startDate": start_date.isoformat(), "endDate": end_date.isoformat(), "api_key": api_key}
                               ) as response:
            data = await response.json()
            print(data)


async def get_cmea(
        api_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    """
    Retrieve data for coronal mass ejection analysis

    :param api_key:
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date is None:
        start_date = date.today() - timedelta(30)

    if end_date is None:
        end_date = date.today()

    async with aiohttp.ClientSession() as session:
        async with session.get(CMEA_URL,
                               params={"startDate": start_date.isoformat(), "endDate": end_date.isoformat(),
                                       "catalog": "ALL", "api_key": api_key, "mostAccurateOnly": True,
                                       }
                               ) as response:
            data = await response.json()
            print(data)


async def get_gs(
        api_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    """
    Retrieve data for geomagnetic storm

    :param api_key:
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date is None:
        start_date = date.today() - timedelta(30)

    if end_date is None:
        end_date = date.today()

    async with aiohttp.ClientSession() as session:
        async with session.get(GS_URL,
                               params={"startDate": start_date.isoformat(), "endDate": end_date.isoformat(), "api_key": api_key}) as response:
            data = await response.json()
            print(data)


async def get_sf(
        api_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
):
    """
    Retrieve data for solar flares

    :param api_key:
    :param start_date:
    :param end_date:
    :return:
    """
    if start_date is None:
        start_date = date.today() - timedelta(30)

    if end_date is None:
        end_date = date.today()

    async with aiohttp.ClientSession() as session:
        async with session.get(FS_URL,
                               params={"startDate": start_date.isoformat(), "endDate": end_date.isoformat(), "api_key": api_key}) as response:
            data = await response.json()
            from pprint import pprint
            pprint(data)


if __name__ == "__main__":
    asyncio.run(get_sf(NASA_API_KEY))