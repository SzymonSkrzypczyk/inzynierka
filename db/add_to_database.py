import csv
from os import getenv
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.inspection import inspect
import dropbox
from db import models_db
from utils import to_bool
from logger import logger

load_dotenv()

DROPBOX_APP_SECRET = getenv("DROPBOX_APP_SECRET")
DROPBOX_APP_KEY = getenv("DROPBOX_APP_KEY")
DROPBOX_REFRESH_TOKEN = getenv("DROPBOX_REFRESH_TOKEN")
DATABASE_URL = getenv("DATABASE_URL")
SEND_RETRY_SLEEP_TIME = 20
MAX_RETRIES = 3
BOOLEAN_COLUMNS = (
    "electron_contaminaton",
    "arcjet_flag"
)

dbx = dropbox.Dropbox(
        app_secret=DROPBOX_APP_SECRET,
        app_key=DROPBOX_APP_KEY,
        oauth2_refresh_token=DROPBOX_REFRESH_TOKEN
)


def save_data_in_db(target_dir: Path, engine: Engine = None, session: Session = None):
    """
    Add data from a given date to the database.

    :param target_dir: Path to the target directory with data to be saved in the DB
    :type target_dir: Path
    :param engine:
    :type engine: Engine
    :param session:
    :type session: Session
    :return:
    """
    logger.log(f"Saving data from {target_dir} to the database")
    if engine is None:
        engine = create_engine(DATABASE_URL, echo=False)
        logger.log_warning("No engine provided, using SQLAlchemy")
    if session is None:
        session = Session(bind=engine)
        logger.log(f"Creating new session with engine: {engine.name}")

    for file in target_dir.iterdir():
        # for each file get its name without suffix and date
        name = file.with_suffix("").name
        name = name[:name.rfind("_")]
        name = name.replace("_", " ").replace("-", " ").title().replace(" ", "")

        try:
            model_class = getattr(models_db, name)
        except AttributeError as e:
            # logger
            logger.log_error(f"No model class found for {name} (from {file.name})")
            raise SystemExit(1) from None

        logger.log(f"Processing {file.name} -> model: {model_class.__name__}")

        with file.open(newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            field_map = {
                c.columns[0].name: c.key
                for c in inspect(model_class).mapper.column_attrs
            }

            objects = []
            for row in reader:
                normalized_row = {}
                for k, v in row.items():
                    if k not in field_map:
                        continue  # ignore unknown fields
                    key = field_map[k]
                    val = to_bool(v) if key in BOOLEAN_COLUMNS else v
                    normalized_row[key] = None if val == "" else val

                try:
                    obj = model_class(**normalized_row)
                    objects.append(obj)
                except Exception as e:
                    logger.log_error(f"Error creating object from row: {row}")
                    logger.log_exception(f"Exception: {e}")
                    raise SystemExit(1) from None
            try:
                session.bulk_save_objects(objects)
            except Exception as e:
                logger.log_error(f"Error saving object from row: {row}")
                logger.log_exception(f"Exception: {e}")

    session.commit()
    session.close()


if __name__ == '__main__':
    ...
