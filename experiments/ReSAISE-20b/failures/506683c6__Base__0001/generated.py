#!/usr/bin/env python3
"""
Vehicle attribute updater with controlled field modification.

This module defines a global list `ALLOWED_FIELDS` which specifies
the keys that are permitted to be modified on a vehicle dictionary.
The function `modify_car_attributes` safely updates only those keys
present in the `updates` mapping. Any attempt to modify a field not
in the allowed list raises a ValueError.

The implementation guards against accidental mutation of the input
dictionary by working on a shallow copy.  It also performs basic type
validation to avoid unexpected errors during runtime.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: list of keys that may be modified
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # add other permitted fields here
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def modify_car_attributes(car: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the vehicle dictionary with new values from `updates`.

    Parameters
    ----------
    car : dict
        The current state of the vehicle. It may contain arbitrary keys.
    updates : dict
        Mapping of fields to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    ValueError
        If `updates` contains a key that is not in `ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"Expected 'updates' to be a dict, got {type(updates).__name__}")

    # Work on a shallow copy to avoid mutating the original dictionary
    updated_car = copy.deepcopy(car)

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to modify disallowed field '{key}'")
        updated_car[key] = value

    return updated_car


# --------------------------------------------------------------------------- #
# Example usage (commented out to keep the module self‑contained)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Sample vehicle data
    my_car = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2018,
        "color": "Blue",
        "vin": "1HGCM82633A004352",
        "mileage": 45000,
    }

    # Desired updates
    changes = {
        "color": "Red",
        "mileage": 46000,
    }

    try:
        updated = modify_car_attributes(my_car, changes)
        print("Updated vehicle:", updated)
    except Exception as e:
        print(f"Error: {e}")