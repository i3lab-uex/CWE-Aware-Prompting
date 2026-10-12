# -*- coding: utf-8 -*-
"""
Vehicle attribute modification module.

This module defines a single function, `modify_car_details`, which safely updates
attributes of a vehicle dictionary. Only attributes listed in the global
`ALLOWED_FIELDS` are permitted to be changed; any attempt to modify a disallowed
field will raise a `ValueError`.  The function is designed with security in mind
to avoid the CWE‑915 vulnerability of uncontrolled attribute modification.
"""

from __future__ import annotations

# List of fields that are allowed to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",          # Vehicle Identification Number
    "owner_id",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update permitted attributes of a vehicle dictionary.

    Parameters
    ----------
    car : dict
        The original vehicle data.  Must be a mapping from string keys to values.
    changes : dict
        Mapping of attribute names to new values that should be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary.  A shallow copy of the original `car`
        is returned; the input object remains unchanged.

    Raises
    ------
    TypeError
        If `car` or `changes` is not a mapping.
    ValueError
        If any key in `changes` is not present in `ALLOWED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of the input `car` to avoid side
      effects on caller data.
    - Only keys listed in :data:`ALLOWED_FIELDS` are permitted for modification,
      protecting against accidental or malicious updates to internal state.
    """
    if not isinstance(car, dict):
        raise TypeError("`car` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    # Create a shallow copy to avoid mutating the caller's object.
    updated_car = car.copy()

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified")
        updated_car[key] = value

    return updated_car