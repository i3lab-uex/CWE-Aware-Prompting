# -*- coding: utf-8 -*-
"""
Vehicle data modification module.

The `modify_vehicle_data` function updates a vehicle's information
dict in a safe and controlled manner. Only keys listed in the global
`ALLOWED_FIELDS` are permitted to be changed; any attempt to modify
other keys will raise a `ValueError`.

The implementation avoids dynamic code execution and ensures that
the input data is not modified in place, thereby preventing accidental
side‑effects.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "registration_state",
)

def modify_vehicle_data(
    vehicle_info: Dict[str, Any],
    changes_to_apply: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary with the vehicle information updated
    according to `changes_to_apply`, but only for keys listed in
    `ALLOWED_FIELDS`.

    Parameters
    ----------
    vehicle_info : dict
        Original vehicle data. Must be a mapping of string keys to any values.
    changes_to_apply : dict
        Desired updates. Keys must be strings and may only include values
        from `ALLOWED_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the original data with any permitted
        updates applied.

    Raises
    ------
    ValueError
        If `changes_to_apply` contains a key not in `ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original dict.
    updated_info = copy.deepcopy(vehicle_info)

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified")
        updated_info[field] = new_value

    return updated_info


# Example usage (for testing purposes only)
if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2015,
        "color": "Blue",
        "vin": "1234567890ABCDEFG",
        "mileage": 65000,
        "registration_state": "CA"
    }

    changes = {
        "color": "Red",
        "mileage": 66000
    }

    print(modify_vehicle_data(original, changes))