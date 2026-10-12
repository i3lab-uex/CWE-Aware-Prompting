#!/usr/bin/env python3
"""
Utility module for safely updating vehicle attributes.

The function `modify_car_attributes` only allows updates to keys
specified in the global list `ALLOWED_FIELDS`. Attempts to modify
any other key will raise a ValueError.

The function returns a new dictionary containing the updated state,
leaving the original `car` object untouched.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define the set of fields that may be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "mileage",
    "engine_type",
    "transmission",
]

# Convert to a set for O(1) membership checks.
_ALLOWED_FIELDS_SET = set(ALLOWED_FIELDS)


def modify_car_attributes(car: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new car dictionary with only allowed fields updated.

    Parameters
    ----------
    car : dict
        The original vehicle attributes.
    updates : dict
        A dictionary containing the fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    TypeError
        If `car` or `updates` is not a dictionary.
    ValueError
        If any key in `updates` is not listed in ALLOWED_FIELDS.

    Notes
    -----
    - The function performs a shallow copy of the original dictionary to avoid
      modifying external references. If any attribute is itself a mutable
      object and needs deep copying, replace `copy.copy` with `copy.deepcopy`.
    - The function does **not** alter the original `car` dictionary.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected `car` to be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"Expected `updates` to be a dict, got {type(updates).__name__}")

    # Start with a shallow copy of the original car.
    updated_car = copy.copy(car)

    for key, value in updates.items():
        if key not in _ALLOWED_FIELDS_SET:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Update the value. This simple assignment handles all JSON-serializable types.
        updated_car[key] = value

    return updated_car