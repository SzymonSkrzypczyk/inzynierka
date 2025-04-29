from typing import Optional, List
from datetime import date, timedelta
import asyncio
import aiohttp
from dotenv import load_dotenv
from os import environ
from response_types import SolarFlare, CoronalMassEjection, CMEAnalyses, CMEInstrument, CoronalMassEjectionAnalysis
from space_weather_retrieval.response_types import GeomagneticStorm

CME_URL = "https://api.nasa.gov/DONKI/CME"
CMEA_URL = "https://api.nasa.gov/DONKI/CMEAnalysis"
GS_URL = "https://api.nasa.gov/DONKI/GST"
FS_URL = "https://api.nasa.gov/DONKI/FLR"


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
            results = [
                CoronalMassEjection(
                    **{k: v for k, v in item.items() if k not in ["cmeAnalyses", "instruments"]},
                    cmeAnalyses=[CMEAnalyses(**cme) for cme in item.get("cmeAnalyses", [])],
                    instruments=[CMEInstrument(**instrument) for instrument in item.get("instruments", [])]
                )
                for item in data
            ]

    return results


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
                                       "catalog": "ALL", "api_key": api_key, "mostAccurateOnly": "True",
                                       }
                               ) as response:
            data = await response.json()

            results = [CoronalMassEjectionAnalysis(**item) for item in data]

    return results


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

            results = [GeomagneticStorm(**item) for item in data]

        return results


async def get_sf(
        api_key: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
) -> List[SolarFlare]:
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
            results = [SolarFlare(**item) for item in data]

    return results


if __name__ == "__main__":
    print(asyncio.run(get_gs(NASA_API_KEY)))