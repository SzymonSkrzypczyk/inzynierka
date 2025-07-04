from os import getenv
from dotenv import load_dotenv
from sqlalchemy import create_engine
from models_db import Base

load_dotenv()
DATABASE_URL = getenv("DATABASE_URL")

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)