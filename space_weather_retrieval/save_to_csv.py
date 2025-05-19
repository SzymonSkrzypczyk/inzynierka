import csv
from typing import Union, List, Any, Dict, Mapping
from datetime import datetime
from pathlib import Path
from pydantic import BaseModel


def _flatten_dict(
    d: Union[Dict[str, Any], List[Any]],
    parent_key: str = "",
    sep: str = "."
) -> Dict[str, Any]:
    """Flatten a nested dictionary or list into a flat dictionary with dot/bracket notation keys."""
    items = []

    if isinstance(d, list):
        for i, v in enumerate(d):
            new_key = f"{parent_key}[{i}]"
            items.extend(_flatten_dict(v, new_key, sep=sep).items() if isinstance(v, (Mapping, list)) else [(new_key, v)])
    elif isinstance(d, dict):
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, (dict, list)):
                items.extend(_flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
    else:
        items.append((parent_key, d))

    return dict(items)


def _model_to_flat_dict(model: BaseModel) -> Dict[str, Any]:
    """Convert a Pydantic model to a flat dictionary."""
    return _flatten_dict(model.model_dump())


def save_to_csv(
        target_name: str,
        target_directory: str,
        data: List[BaseModel]
) -> None:
    """Save a list of Pydantic models to a CSV with flattened fields."""
    flat_dicts = [_model_to_flat_dict(model) for model in data]
    fieldnames = sorted({key for d in flat_dicts for key in d})

    output_path = Path(target_directory) / f"{target_name}_{datetime.today().strftime('%d_%m_%Y')}.csv"

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_dicts)
