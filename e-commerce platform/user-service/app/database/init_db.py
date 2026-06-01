import time

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.database.database import engine


def wait_for_db():

    retries = 30

    while retries > 0:

        try:
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