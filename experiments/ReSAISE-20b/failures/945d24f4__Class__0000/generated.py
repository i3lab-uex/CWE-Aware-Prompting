# -*- coding: utf-8 -*-
"""
Utility module for updating car information.

This module defines a single public function, `update_car_information`, which
applies a set of changes to an existing car details dictionary. Only the keys
listed in the global `ALLOWED_FIELDS` list are permitted to be updated.

The implementation guards against accidental modification of non‑allowed
attributes and ensures that the input dictionary is not mutated in place.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List


# List of fields that are allowed to be updated.
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",          # Vehicle Identification Number
    "engine_type",
    "transmission",
]


def update_car_information(
    car_details: Dict[str, Any],
    changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary containing the updated car details.

    Parameters
    ----------
    car_details : dict
        Dictionary representing the current state of a vehicle. The dictionary
        may contain arbitrary keys, but only those present in `ALLOWED_FIELDS`
        are eligible for modification.
    changes : dict
        Dictionary mapping field names to new values. Only keys that appear in
        `ALLOWED_FIELDS` are considered; all other keys raise a ValueError.

    Returns
    -------
    dict
        A new dictionary with the requested updates applied. The original
        `car_details` is left untouched.

    Raises
    ------
    ValueError
        If `changes` contains any key that is not in `ALLOWED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of the original dictionary to avoid
      mutating external state.
    - Nested mutable objects are not deep‑copied; callers should avoid
      modifying nested structures directly if isolation is required.
    """
    # Validate input types
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Check for disallowed fields
    invalid_keys = [key for key in changes if key not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"The following fields are not allowed to be updated: {invalid_keys}"
        )

    # Create a shallow copy of the original details
    updated = copy.deepcopy(car_details)

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated


# Example usage (commented out to avoid execution during import)
if __name__ == "__main__":
    car = {"make": "Toyota", "model": "Camry", "year": 2018, "color": "blue"}
    try:
        new_car = update_car_information(car, {"year": 2020, "color": "red"})
        print(new_car)
    except Exception as exc:
        print(f"Error: {exc}")