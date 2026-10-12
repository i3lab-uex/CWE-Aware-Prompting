# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle information.

This module defines a global list `ALLOWED_FIELDS` containing the names of
attributes that may be updated on a vehicle dictionary. The function
`adjust_vehicle_info` updates only those attributes that are present in this
list, raising a `ValueError` if any requested modification is not permitted.
"""

from __future__ import annotations

from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "owner",
    # Add other allowed fields here
]


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_vehicle_info(
    auto: Dict[str, Any], modifications: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with permitted modifications.

    Parameters
    ----------
    auto : dict
        The original vehicle dictionary. It will be updated in place.
    modifications : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (same object as ``auto``).

    Raises
    ------
    TypeError
        If *auto* or *modifications* is not a dictionary.
    ValueError
        If any key in *modifications* is not present in ``ALLOWED_FIELDS``.
    """
    if not isinstance(auto, dict):
        raise TypeError(f"'auto' must be a dict, got {type(auto).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(
            f"'modifications' must be a dict, got {type(modifications).__name__}"
        )

    # Filter modifications to allowed fields
    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be modified. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )
        auto[key] = value

    return auto


# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "color": "red",
    }

    try:
        updated = adjust_vehicle_info(
            vehicle,
            {"color": "blue", "year": 2016, "owner": "Alice"},
        )
        print("Updated vehicle:", updated)
    except Exception as exc:
        print(f"Error: {exc}")