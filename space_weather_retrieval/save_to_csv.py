from datetime import date
from typing import Union, List, Iterable
from pathlib import Path
import csv


def save_to_csv(
        target_name: str,
        target_directory: Union[str, Path],
        data: Union[List, Iterable]
):
    """
    Serialize and save a list of dataclasses to a CSV file with flattened nested fields
    """
    target_directory = Path(target_directory)
    target_directory.mkdir(exist_ok=True)

    target_name = f"{target_name.removesuffix(".csv")}_{date.today().isoformat()}.csv"
    final_target_location = target_directory / target_name
    final_target_location.touch(exist_ok=True)

    flattened_data = [item.serialize() for item in data]
    fieldnames = sorted({key for row in flattened_data for key in row.keys()})

    with final_target_location.open(mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flattened_data)
