from typing import Union, List, Iterable
from pathlib import Path
import csv


def save_to_csv(
        target_name: Union[str, Path],
        target_directory: Union[str, Path],
        data: Union[List, Iterable]
):
    """

    :param target_name:
    :param target_directory:
    :param data:
    :return:
    """
    # create target_directory if it does not exist
    target_directory.mkdir(exist_ok=True)
    # create target_file if it does not exist
    final_target_location = target_directory / (target_name if target_name.endswith(".csv") else f"{target_name}.csv")
    final_target_location.touch(exist_ok=True)

    with target_name.open(mode="w", newline="", encoding="utf-8") as file:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)
