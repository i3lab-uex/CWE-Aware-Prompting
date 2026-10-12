#!/usr/bin/env python3
"""
Utility for updating vehicle (auto) details.

Only keys listed in the global ``ALLOWED_FIELDS`` are permitted to be
modified.  Any attempt to change a disallowed field raises a ``ValueError``.
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
    "engine_type",
    "transmission",
    "fuel_type",
]

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def modify_auto_data(
    auto_details: Dict[str, Any], field_updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Update allowed fields in a vehicle's details dictionary.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle data.
    field_updates : dict
        Dictionary with keys to update and their new values.

    Returns
    -------
    dict
        The updated vehicle details dictionary.

    Raises
    ------
    TypeError
        If either argument is not a ``dict``.
    ValueError
        If any key in ``field_updates`` is not present in ``ALLOWED_FIELDS``.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Perform updates
    for key, value in field_updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        auto_details[key] = value

    return auto_details


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_auto = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2018,
        "color": "Blue",
        "vin": "1NXBR32E64Z123456",
    }

    updates = {"color": "Red", "year": 2019}

    try:
        updated_auto = modify_auto_data(sample_auto, updates)
        print("Updated vehicle data:", updated_auto)
    except Exception as exc:
        print(f"Error: {exc}")