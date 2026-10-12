#!/usr/bin/env python3
"""
Vehicle data modification module.

This module provides a single function, `modify_vehicle_data`, that safely updates
a vehicle information dictionary. Only keys listed in the global `ALLOWED_FIELDS`
are permitted to be modified, mitigating CWE-915 risks.

Author: ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Allowed fields that can be updated.  Extend this list as needed.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(vehicle_info: dict, changes_to_apply: dict) -> dict:
    """
    Return a new dictionary with updates applied to allowed fields.

    Parameters
    ----------
    vehicle_info : dict
        Original vehicle data. Must contain string keys and JSON‑serialisable values.
    changes_to_apply : dict
        Proposed updates. Only keys present in ALLOWED_FIELDS will be applied.

    Returns
    -------
    dict
        A new dictionary with the updates merged into a copy of `vehicle_info`.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `changes_to_apply` contains no keys that are allowed to be modified.
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(changes_to_apply, dict):
        raise TypeError("changes_to_apply must be a dictionary")

    # Determine which keys are both present in changes and allowed
    valid_updates = {k: v for k, v in changes_to_apply.items() if k in ALLOWED_FIELDS}

    if not valid_updates:
        raise ValueError("No valid fields to update")

    # Create a shallow copy to avoid mutating the original dictionary
    updated_info = vehicle_info.copy()
    updated_info.update(valid_updates)

    return updated_info

# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    original = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2010,
        "color": "Blue",
        "vin": "123ABC456DEF"
    }
    changes = {
        "color": "Red",
        "year": 2011,
        "driver_license": "XYZ"   # not allowed
    }

    try:
        new_data = modify_vehicle_data(original, changes)
        print("Updated vehicle data:", new_data)
    except Exception as exc:
        print(f"Error: {exc}")