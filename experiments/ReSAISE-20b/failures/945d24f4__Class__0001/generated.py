# -*- coding: utf-8 -*-
"""
Vehicle data updater.

This module defines a single function `update_car_information` that safely
updates only the fields listed in the global ``ALLOWED_FIELDS`` list.  It
prevents accidental or malicious modification of arbitrary keys, guarding
against CWE‑913 (Improper Control of Dynamically‑Managed Code Resources).
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Global configuration – only these keys may be changed by the updater.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "mileage",
    "engine_type",
    "transmission",
    "fuel_type",
    # Add more allowed fields as needed.
]

# --------------------------------------------------------------------------- #
#  Public API
# --------------------------------------------------------------------------- #
def update_car_information(
    car_details: Dict[str, Any],
    changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle's details safely.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing vehicle information.  This dictionary
        is modified in place.
    changes : dict
        A mapping of field names to new values.  Only keys present in the
        global ``ALLOWED_FIELDS`` list will be applied.

    Returns
    -------
    dict
        The updated ``car_details`` dictionary (the same object that was passed
        in).

    Raises
    ------
    TypeError
        If either ``car_details`` or ``changes`` is not a dictionary.
    ValueError
        If an attempt is made to update a field that is not in ``ALLOWED_FIELDS``.
    """
    # Basic type checks to guard against accidental misuse
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Iterate over the provided changes
    for key, value in changes.items():
        if not isinstance(key, str):
            raise ValueError(f"Field name must be a string; got {type(key).__name__}")

        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated")

        # Apply the change – simple assignment suffices.
        car_details[key] = value

    return car_details


# --------------------------------------------------------------------------- #
#  Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
# if __name__ == "__main__":
#     car = {
#         "make": "Toyota",
#         "model": "Corolla",
#         "year": 2018,
#         "color": "Blue",
#     }
#
#     updates = {
#         "year": 2020,
#         "color": "Red",
#         "vin": "123ABC456DEF",  # Allowed
#     }
#
#     updated_car = update_car_information(car, updates)
#     print(updated_car)