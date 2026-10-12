#!/usr/bin/env python3
"""
Vehicle information updater.

This module provides a single function `update_vehicle_info` that safely updates
attributes of a vehicle dictionary. Only fields listed in the global
`ALLOWED_FIELDS` constant are permitted to be modified. Any attempts to change
other attributes are silently ignored, preventing accidental or malicious
alterations.

The function does not perform any dynamic code execution and is safe from the
CWE-913 vulnerability.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Global configuration: list of attributes that can be updated.
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

# --------------------------------------------------------------------------- #
def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with allowed attributes updated.

    Parameters
    ----------
    vehicle : dict
        Original vehicle data. Must be a mapping from string keys to any values.
    updates : dict
        Proposed changes. Keys are attribute names, values are the new values.

    Returns
    -------
    dict
        A shallow copy of `vehicle` with any allowed fields replaced by the values in `updates`.

    Notes
    -----
    * Only keys present in :data:`ALLOWED_FIELDS` are applied.
    * The original `vehicle` dictionary is **not** modified.
    * If an update contains a key not in :data:`ALLOWED_FIELDS`, it is ignored.
    """
    # Create a shallow copy to avoid mutating the input dictionary
    updated_vehicle = copy.copy(vehicle)

    for key, value in updates.items():
        if key in ALLOWED_FIELDS:
            updated_vehicle[key] = value
    return updated_vehicle

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    vehicle_data = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "owner": "Alice",
        "registration": "XYZ1234",
        "color": "red",  # not allowed to be updated
    }

    new_values = {
        "year": 2020,
        "owner": "Bob",
        "color": "blue",   # will be ignored
    }

    updated = update_vehicle_info(vehicle_data, new_values)
    print("Original:", vehicle_data)
    print("Updated :", updated)