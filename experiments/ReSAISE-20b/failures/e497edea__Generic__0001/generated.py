# -*- coding: utf-8 -*-

"""
Vehicle information updater.

The module defines a single public function `adjust_vehicle_info` which
updates only the attributes of a vehicle dictionary that are listed in
the global `ALLOWED_FIELDS`. Attempting to modify any other attribute
raises a ValueError.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# List of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "owner",
]

def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update the vehicle dictionary `auto` with values from `modifications`.

    Parameters
    ----------
    auto : dict
        Dictionary representing the vehicle.
    modifications : dict
        Mapping of attribute names to new values that should be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function performs a shallow copy of `auto` to avoid mutating the
    original dictionary unless that is explicitly desired by the caller.
    """
    if not isinstance(auto, dict):
        raise TypeError("`auto` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    # Create a copy to avoid side effects on the caller's dict.
    updated = auto.copy()

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        updated[key] = value

    return updated