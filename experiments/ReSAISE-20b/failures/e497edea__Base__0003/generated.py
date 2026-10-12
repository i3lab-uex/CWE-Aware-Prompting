# -*- coding: utf-8 -*-

"""
Vehicle attribute updater.

This module defines a global list `ALLOWED_FIELDS` that enumerates the
vehicle attributes that are permitted to be modified.  The function
`adjust_vehicle_info` takes a vehicle dictionary and a set of desired
updates, applies only the allowed changes, and returns the updated
dictionary.

Security note:
    * Only keys present in `ALLOWED_FIELDS` are accepted.
    * Any attempt to modify a disallowed field raises a ValueError,
      preventing unintended or malicious changes.
"""

from __future__ import annotations

# List of vehicle attributes that may be updated.  Add or remove
# entries as the domain model evolves.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    # Add more permitted fields here
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update a vehicle dictionary with the supplied modifications.

    Parameters
    ----------
    auto : dict
        The original vehicle data.  Must be a mapping of attribute names to values.
    modifications : dict
        Keys are the attributes to change, and values are the new values.

    Returns
    -------
    dict
        The vehicle dictionary after applying permitted updates.

    Raises
    ------
    TypeError
        If `auto` or `modifications` is not a dictionary.
    ValueError
        If any key in `modifications` is not listed in `ALLOWED_FIELDS`.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"Expected `auto` to be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"Expected `modifications` to be a dict, got {type(modifications).__name__}")

    # Create a shallow copy so the caller's dictionary is not modified in place
    updated_auto = auto.copy()

    for field, new_value in modifications.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to modify disallowed field '{field}'")
        updated_auto[field] = new_value

    return updated_auto