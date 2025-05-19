from pathlib import Path
from typing import Union
from os import getenv
from dotenv import load_dotenv
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError, ApiError
from logger import Logger

load_dotenv()

DROPBOX_API_KEY = getenv("DROPBOX_API_KEY")


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
    dbx = dropbox.Dropbox(DROPBOX_API_KEY)

    with open(archive_path, "rb") as f:
        logger.log(f"Uploading {archive_path} to Dropbox at {dropbox_path}")
        try:
            dbx.files_upload(f.read(), dropbox_path, mode=WriteMode('overwrite'))
        except ApiError as e:
            logger.log_exception(f"API error: {e}")
            return
        except AuthError as e:
            logger.log_exception(f"Authentication error: {e}")
            return

        logger.log(f"Successfully uploaded {archive_path} to Dropbox at {dropbox_path}")
