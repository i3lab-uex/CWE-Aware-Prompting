# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

The module defines a global list `ALLOWED_FIELDS` that specifies which
keys in a vehicle dictionary may be altered.  The function
`modify_vehicle_data()` applies changes only to those keys and returns a
new dictionary with the updates applied.  Attempts to modify disallowed
keys raise a `ValueError`.

This implementation protects against CWE-913 by explicitly restricting
which fields may be updated, preventing arbitrary code execution or
tampering with internal state.
"""

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
]

def modify_vehicle_data(
    vehicle_info: dict,
    changes_to_apply: dict
) -> dict:
    """
    Return a new dictionary with updates applied to allowed fields.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.
    changes_to_apply : dict
        Mapping of fields to new values.  Only keys present in
        `ALLOWED_FIELDS` are applied.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If `changes_to_apply` contains a key not in `ALLOWED_FIELDS`.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Create a shallow copy to avoid mutating the original dict
    updated = vehicle_info.copy()

    for field, new_value in changes_to_apply.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified")
        updated[field] = new_value

    return updated