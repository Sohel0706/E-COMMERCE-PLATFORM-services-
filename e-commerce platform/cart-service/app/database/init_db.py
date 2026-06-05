import time

from sqlalchemy import text
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from app.database.database import DB_NAME
from app.database.database import SERVER_DATABASE_URL
from app.database.database import engine


def wait_for_db():
    retries = 30

    while retries > 0:
        try:
            create_database_if_missing()

            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print("Database connected")
            return

        except OperationalError:
            print(
                "Database unavailable. "
                "Retrying..."
            )

            retries -= 1
            time.sleep(2)

    raise Exception("Database unavailable")


def create_database_if_missing():
    if not DB_NAME.replace("_", "").isalnum():
        raise ValueError("Invalid database name")

    server_engine = create_engine(
        SERVER_DATABASE_URL,
        isolation_level="AUTOCOMMIT"
    )

    with server_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`"))
