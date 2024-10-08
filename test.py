"""
Test validations.
"""

import argparse
import os
import json
from typing import Any
from src.spacex import SpaceX
import tempfile


def parse_args() -> str:
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bazel", action="store_true")
    args = parser.parse_args()
    return args.bazel


def pretty_print(obj: Any, overwrite: bool = False, bazel: bool = False) -> None:
    """
    Pretty print.
    """
    if bazel:
        pretty_print_bazel(obj, overwrite)
    else:
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


def pretty_print_bazel(obj: Any, overwrite: bool = False) -> None:
    if not obj:
        return
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        jsonified = json.dumps(obj=obj, indent=2)
        print(jsonified)
        temp_file.write(jsonified + "\n")
        if isinstance(obj, list):
            len_msg = f"Array Length: {len(obj)}"
            print(len_msg)
            temp_file.write(len_msg + "\n")


def test_company(s: SpaceX, bazel: bool = False) -> None:
    company = s.invoke(entity="company")
    pretty_print(company, overwrite=True, bazel=bazel)
    assert isinstance(company, dict)


def test_ships(s: SpaceX, bazel: bool = False) -> None:
    s.invoke(
        entity="ships", paginate=True, identifier="5ea6ed2e080df4000697c90a"
    )  # WARNING Too many arguments
    ships = s.invoke(entity="ships", paginate=True)
    pretty_print(ships, bazel=bazel)
    assert isinstance(ships, list)
    ship = s.invoke(entity="ships", identifier="5ea6ed2e080df4000697c90a")
    pretty_print(ship, bazel=bazel)
    assert isinstance(ship, dict)


def test_launches(s: SpaceX, bazel: bool = False) -> None:
    s.invoke(
        entity="launches",
        paginate=True,
        identifier="5ea6ed2e080df4000697c90a",
        dates=("2020-04-01", "2020-06-30"),
    )  # WARNING Too many arguments
    batch_1 = s.invoke(
        entity="launches", dates=("2020-04-01", "2020-04-30")
    )  # 1 launch
    pretty_print(batch_1, bazel=bazel)
    batch_2 = s.invoke(
        entity="launches", dates=("2020-05-01", "2020-05-31")
    )  # 1 launch
    pretty_print(batch_2, bazel=bazel)
    batch_3 = s.invoke(
        entity="launches", dates=("2020-06-01", "2020-06-30")
    )  # 2 launches
    pretty_print(batch_3, bazel=bazel)
    batch_all = s.invoke(
        entity="launches", dates=("2020-04-01", "2020-06-30")
    )  # 4 launches
    pretty_print(batch_all, bazel=bazel)
    assert (
        isinstance(batch_1, list)
        and isinstance(batch_2, list)
        and isinstance(batch_3, list)
        and isinstance(batch_all, list)
        and len(batch_1) + len(batch_2) + len(batch_3) == len(batch_all)
    )


def test_landpads(s: SpaceX, bazel: bool = False) -> None:
    landpads = s.invoke(entity="landpads", paginate=True)
    pretty_print(landpads, bazel=bazel)
    assert isinstance(landpads, list)
    landpad = s.invoke(entity="landpads", identifier="5e9e3033383ecb075134e7cd")
    pretty_print(landpad, bazel=bazel)
    assert isinstance(landpad, dict)


def test_starlink(s: SpaceX, bazel: bool = False) -> None:
    s.invoke(
        entity="starlink", paginate=True, identifier="5ea6ed2e080df4000697c90a"
    )  # WARNING Too many arguments
    satellites = s.invoke(entity="starlink", paginate=True)
    pretty_print(satellites, bazel=bazel)
    assert isinstance(satellites, list)
    satellite = s.invoke(entity="starlink", identifier="5eed770f096e59000698560d")
    pretty_print(satellite, bazel=bazel)
    assert isinstance(satellite, dict)


def run_tests(bazel: bool = False) -> None:
    spacex = SpaceX()
    test_company(spacex, bazel=bazel)
    test_ships(spacex, bazel=bazel)
    test_launches(spacex, bazel=bazel)
    test_landpads(spacex, bazel=bazel)
    test_starlink(spacex, bazel=bazel)
    print("All tests passed :)")


if __name__ == "__main__":
    bazel = parse_args()
    run_tests(bazel=bazel)
