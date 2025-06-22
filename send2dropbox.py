from time import sleep
from pathlib import Path
from typing import Union
from os import getenv
from dotenv import load_dotenv
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError, ApiError
from logger import Logger

load_dotenv()

DROPBOX_APP_SECRET = getenv("DROPBOX_APP_SECRET")
DROPBOX_APP_KEY = getenv("DROPBOX_APP_KEY")
DROPBOX_REFRESH_TOKEN = getenv("DROPBOX_REFRESH_TOKEN")
SEND_RETRY_SLEEP_TIME = 20
MAX_RETRIES = 3


def send_to_dropbox(
    archive_path: Union[str, Path],
    dropbox_path: str,
    logger: Logger
):
    """
    Upload a file to Dropbox

    :param archive_path: Path to the file to be uploaded
    :param dropbox_path: Path in Dropbox where the file will be uploaded
    :param logger: Logger instance for logging
    """
    dbx = dropbox.Dropbox(
        app_secret=DROPBOX_APP_SECRET,
        app_key=DROPBOX_APP_KEY,
        oauth2_refresh_token=DROPBOX_REFRESH_TOKEN
    )
    retries = 0

    with open(archive_path, "rb") as f:
        logger.log(f"Uploading {archive_path} to Dropbox at {dropbox_path}")
        while retries < MAX_RETRIES:
            try:
                dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))

                logger.log(f"Successfully uploaded {archive_path} to Dropbox at {dropbox_path}")
            except ApiError as e:
                logger.log_exception(f"API error: {e}")
                retries += 1
                logger.log(f"Sleeping for {SEND_RETRY_SLEEP_TIME} seconds before retrying")
                sleep(SEND_RETRY_SLEEP_TIME)

            except AuthError as e:
                logger.log_exception(f"Authentication error: {e}")
                retries += 1
                logger.log(f"Sleeping for {SEND_RETRY_SLEEP_TIME} seconds before retrying")
                sleep(SEND_RETRY_SLEEP_TIME)
        else:
            logger.log_error(f"Failed to upload {archive_path} to Dropbox after {MAX_RETRIES} retries")
            raise Exception(f"Failed to upload {archive_path} to Dropbox after {MAX_RETRIES} retries")
