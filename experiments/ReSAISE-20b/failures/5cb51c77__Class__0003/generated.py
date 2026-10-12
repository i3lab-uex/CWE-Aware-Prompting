#!/usr/bin/env python3
"""
Utility module for safely modifying vehicle data.

The function `modify_vehicle_data` updates only the fields that are explicitly
listed in the global `ALLOWED_FIELDS` list.  This prevents accidental or
malicious changes to other attributes of the vehicle dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Global configuration: list of fields that may be updated
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "registration_expiry",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_vehicle_data(
    vehicle_info: Dict[str, Any], changes_to_apply: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary with updates applied only to allowed fields.

    Parameters
    ----------
    vehicle_info : dict
        Original vehicle data.
    changes_to_apply : dict
        Mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        A copy of `vehicle_info` with the allowed changes applied.

    Raises
    ------
    ValueError
        If any key in `changes_to_apply` is not present in `ALLOWED_FIELDS`.
    TypeError
        If the input arguments are not dictionaries.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Work on a shallow copy to avoid mutating the original dict
    updated_info = copy.deepcopy(vehicle_info)

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be updated.")
        # Optional: add type validation here if desired
        updated_info[field] = new_value

    return updated_info


# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Sample vehicle data
    sample_vehicle = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "color": "Blue",
        "vin": "123ABC456DEF78901",
        "mileage": 15000,
        "registration_expiry": "2025-12-31",
    }

    # Desired changes
    updates = {"color": "Red", "year": 2021}

    try:
        new_vehicle = modify_vehicle_data(sample_vehicle, updates)
        print("Updated vehicle:", new_vehicle)
    except Exception as exc:
        print(f"Error updating vehicle: {exc}")