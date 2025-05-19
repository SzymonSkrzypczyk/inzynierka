import csv
from typing import Union, List, Any, Dict, Mapping
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


def _flatten_dict(
    dictionary: Union[Dict[str, Any], List[Any]],
    parent_key: str = "",
    sep: str = "."
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary or list into a flat dictionary with dot/bracket notation keys.

    :param dictionary: Dictionary or list to flatten
    :type dictionary: Union[Dict[str, Any], List[Any]]
    :param parent_key: Base key string for the current level
    :type parent_key: str
    :param sep: Separator to use for flattening
    :type sep: str

    :return: Flattened dictionary
    :rtype: Dict[str, Any]
    """
    items = []

    if isinstance(dictionary, list):
        for i, v in enumerate(dictionary):
            new_key = f"{parent_key}[{i}]"
            items.extend(_flatten_dict(v, new_key, sep=sep).items() if isinstance(v, (Mapping, list)) else [(new_key, v)])
    elif isinstance(dictionary, dict):
        for k, v in dictionary.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(_flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, dictionary))

    return dict(items)


def _model_to_flat_dict(model: BaseModel) -> Dict[str, Any]:
    """
    Convert a Pydantic model to a flat dictionary.

    :param model: Pydantic model instance
    :type model: BaseModel

    :return: Flat dictionary representation of the model
    :rtype: Dict[str, Any]
    """
    return _flatten_dict(model.model_dump())


def save_to_csv(
        target_name: str,
        target_directory: str,
        data: List[BaseModel]
) -> None:
    """
    Save a list of Pydantic models to a CSV with flattened fields.

    :param target_name: Name of the target CSV file
    :type target_name: str
    :param target_directory: Directory where the CSV file will be saved
    :type target_directory: str
    :param data: List of Pydantic models to be saved
    :type data: List[BaseModel]

    :return: None
    """
    flat_dicts = [_model_to_flat_dict(model) for model in data]
    fieldnames = sorted({key for d in flat_dicts for key in d})

    output_path = Path(target_directory) / f"{target_name}_{datetime.today().strftime('%d_%m_%Y')}.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_dicts)
