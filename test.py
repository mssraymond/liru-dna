"""
Test validations.
"""

import os
import json
from typing import Any
from src.spacex import SpaceX


def pretty_print(obj: Any, overwrite: bool = False) -> None:
    """
    Pretty print.
    """
    if not obj:
        return
    with open(
        os.path.join("test_output/test_result.txt"),
        mode="w" if overwrite else "a",
        encoding="utf-8",
    ) as file:
        jsonified = json.dumps(obj=obj, indent=2)
        print(jsonified)
        file.write(jsonified + "\n")
        if isinstance(obj, list):
            len_msg = f"Array Length: {len(obj)}"
            print(len_msg)
            file.write(len_msg + "\n")


def test_company(s: SpaceX) -> None:
    company = s.invoke(entity="company")
    pretty_print(company, overwrite=True)
    assert isinstance(company, dict)


def test_ships(s: SpaceX) -> None:
    s.invoke(
        entity="ships", paginate=True, identifier="5ea6ed2e080df4000697c90a"
    )  # WARNING Too many arguments
    ships = s.invoke(entity="ships", paginate=True)
    pretty_print(ships)
    assert isinstance(ships, list)
    ship = s.invoke(entity="ships", identifier="5ea6ed2e080df4000697c90a")
    pretty_print(ship)
    assert isinstance(ship, dict)


def test_launches(s: SpaceX) -> None:
    s.invoke(
        entity="launches",
        paginate=True,
        identifier="5ea6ed2e080df4000697c90a",
        dates=("2020-04-01", "2020-06-30"),
    )  # WARNING Too many arguments
    batch_1 = s.invoke(
        entity="launches", dates=("2020-04-01", "2020-04-30")
    )  # 1 launch
    pretty_print(batch_1)
    batch_2 = s.invoke(
        entity="launches", dates=("2020-05-01", "2020-05-31")
    )  # 1 launch
    pretty_print(batch_2)
    batch_3 = s.invoke(
        entity="launches", dates=("2020-06-01", "2020-06-30")
    )  # 2 launches
    pretty_print(batch_3)
    batch_all = s.invoke(
        entity="launches", dates=("2020-04-01", "2020-06-30")
    )  # 4 launches
    pretty_print(batch_all)
    assert (
        isinstance(batch_1, list)
        and isinstance(batch_2, list)
        and isinstance(batch_3, list)
        and isinstance(batch_all, list)
        and len(batch_1) + len(batch_2) + len(batch_3) == len(batch_all)
    )


def test_landpads(s: SpaceX) -> None:
    landpads = s.invoke(entity="landpads", paginate=True)
    pretty_print(landpads)
    assert isinstance(landpads, list)
    landpad = s.invoke(entity="landpads", identifier="5e9e3033383ecb075134e7cd")
    pretty_print(landpad)
    assert isinstance(landpad, dict)


def test_starlink(s: SpaceX) -> None:
    s.invoke(
        entity="starlink", paginate=True, identifier="5ea6ed2e080df4000697c90a"
    )  # WARNING Too many arguments
    satellites = s.invoke(entity="starlink", paginate=True)
    pretty_print(satellites)
    assert isinstance(satellites, list)
    satellite = s.invoke(entity="starlink", identifier="5eed770f096e59000698560d")
    pretty_print(satellite)
    assert isinstance(satellite, dict)


def run_tests() -> None:
    spacex = SpaceX()
    test_company(spacex)
    test_ships(spacex)
    test_launches(spacex)
    test_landpads(spacex)
    test_starlink(spacex)
    print("All tests passed :)")


if __name__ == "__main__":
    run_tests()
