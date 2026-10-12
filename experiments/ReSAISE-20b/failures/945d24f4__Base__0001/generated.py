#!/usr/bin/env python3
"""
Module: car_update

Provides a secure function to update vehicle details while restricting modifications
to a predefined set of allowed fields.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# Global list of fields that are allowed to be updated.
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "transmission",
    "fuel_type",
]


def update_car_information(
    car_details: Dict[str, Any], changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary containing the updated car details.

    Parameters
    ----------
    car_details : dict
        Original vehicle information. Must not be modified in place.
    changes : dict
        Proposed updates. Only keys present in ALLOWED_FIELDS are applied.

    Returns
    -------
    dict
        A new dictionary with the updates applied.

    Raises
    ------
    ValueError
        If any key in ``changes`` is not present in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of ``car_details`` to avoid mutating the
      caller's data.
    * Only keys in ``ALLOWED_FIELDS`` are permitted; attempting to update any
      other key results in a ValueError.
    """
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Identify any disallowed fields
    disallowed = [k for k in changes if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to update disallowed fields: {', '.join(disallowed)}"
        )

    # Create a shallow copy to avoid side effects
    updated = copy.deepcopy(car_details)

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated


# Example usage (for testing purposes only; remove or guard under __name__ == "__main__")
if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "color": "blue",
        "vin": "123456789ABCDEFG",
    }

    updates = {"color": "red", "mileage": 15000}
    try:
        new_car = update_car_information(original, updates)
        print("Updated car:", new_car)
    except Exception as e:
        print(f"Error: {e}")