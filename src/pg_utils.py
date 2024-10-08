"""
Utility class to work with PostgreSQL DB.
"""

from typing import Any
from psycopg2 import connect
from psycopg2.extras import Json
from src.logger import Logger


class PostgreSQL:
    """
    Utility class to abstract away `psycopg2` module.
    """

    def __init__(self) -> None:
        self.logger = Logger()
        self.conn = None
        self.cur = None

    def pg_connect(self) -> None:
        """
        Connect to PostgreSQL DB with hardcoded credentials.
        Obviously NOT representative of production setup.
        """
        conn = connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="postgres",
            port="5432",
        )
        self.conn = conn
        self.cur = conn.cursor()
        self.logger.info("Connection successfully established.")

    def ingest_data(self, data: Any, table_name: str):
        assert self.cur
        self.logger.info(f"Ingesting '{table_name}' data...")
        self.cur.execute(
            f"DROP TABLE IF EXISTS public.{table_name}"
        )  # Reset and recreate
        self.cur.execute(
            f"CREATE TABLE IF NOT EXISTS public.{table_name} (json_data JSON)"
        )
        insert_sql = f"INSERT INTO public.{table_name} VALUES (%s)"
        if isinstance(data, dict):
            self.cur.execute(query=insert_sql, vars=(Json(data),))
        if isinstance(data, list):
            self.cur.executemany(
                query=insert_sql, vars_list=[(Json(datum),) for datum in data]
            )
        self.logger.info(f"'{table_name}' data successfully ingested.")

    def pg_close(self) -> None:
        assert self.conn and self.cur
        self.conn.commit()
        self.conn.close()
        self.logger.info("Connection successfully closed.")
