from pathlib import Path
from typing import Union
from shutil import rmtree
import logging
from os import environ
from datetime import date, datetime
import requests
from dotenv import load_dotenv

load_dotenv()
NASA_API_KEY = environ["NASA_API_KEY"]
NASA_API_ENDPOINT = "https://api.nasa.gov/planetary/earth/imagery"
KRAKOW_LATITUDE = 50.049683
KRAKOW_LONGITUDE = 19.944544
DEFAULT_DIM = 0.1
DATE_FORMAT = "%Y-%m-%d"
TARGET_SAVE_DIRECTORY = Path(__file__).parent / "images"


def get_image(
        lon: float = KRAKOW_LONGITUDE,
        lat: float = KRAKOW_LATITUDE,
        target_date: str = date.today().strftime(DATE_FORMAT),
        image_dim: float = DEFAULT_DIM,
        api_key: str = NASA_API_KEY
) -> bytes:
    """
    Function responsible for calling NASA API and sequentially returning a requested satellite image

    :param lon: longitude of a target place
    :type lon: float
    :param lat: latitude of a target place
    :type lat: float
    :param target_date: date of capturing an image
    :type target_date: str
    :param image_dim: width and height of image in degrees
    :type image_dim: float
    :param api_key: key to the NASA REST API
    :type api_key: str

    :return: Returns a satellite image of requested area
    :rtype: bytes
    """
    res = requests.get(NASA_API_ENDPOINT, params={
        "lon": lon,
        "lat": lat,
        "api_key": api_key,
        "date": target_date,
        "dim": image_dim
    })

    if not res.status_code == 200:
        raise ValueError("The request has not been finished successfully") from None

    return res.content


def save_image(
        content: bytes,
        target_date: str = date.today().strftime(DATE_FORMAT),
        target_directory: Union[str, Path] = TARGET_SAVE_DIRECTORY
) -> None:
    """
    Saves a returned image inside a directory corresponding to the day of image's origin

    :param content: image returned by NASA API
    :type content: bytes
    :param target_date: day the image has been taken
    :type target_date: str
    :param target_directory: directory containing all the images
    :type target_directory: Union[str, Path]
    :return:
    """
    # create the directory if it does not already exist
    target_directory.mkdir(exist_ok=True)

    # create a directory for a given day
    day_directory = target_directory / target_date
    # ensure there is always only one file within a directory
    if day_directory.exists():
        rmtree(day_directory)
    day_directory.mkdir(exist_ok=True)

    # save the file inside the day_directory
    target_file = day_directory / f"{target_date}_on_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png"
    target_file.touch()
    # write the image itself
    target_file.write_bytes(content)


if __name__ == '__main__':
    image = get_image()
    save_image(image)
