"""
Ingest SpaceX data into PostgreSQL DB.
"""

from src.spacex import SpaceX
from src.pg_utils import PostgreSQL


def main():
    spacex = SpaceX()
    postgres = PostgreSQL()
    postgres.pg_connect()
    for entity in ("company", "ships", "landpads", "launches", "starlink"):
        data = spacex.invoke(entity=entity, paginate=entity != "company")
        postgres.ingest_data(
            data=data,
            table_name=(
                "satellite" if entity == "starlink" else entity.rstrip("s").rstrip("e")
            ),
        )
    postgres.pg_close()


if __name__ == "__main__":
    main()
