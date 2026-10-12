# -*- coding: utf-8 -*-
"""
Utility module for safely updating vehicle data dictionaries.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global list of fields that are allowed to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    "mileage",
    # Add other allowed fields here
]


def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with selected fields from ``field_updates`` applied
    to ``auto_details``. Only keys listed in :data:`ALLOWED_FIELDS` are updated.

    Parameters
    ----------
    auto_details:
        Dictionary representing the vehicle's current details.
    field_updates:
        Dictionary of fields to update with their new values.

    Returns
    -------
    dict
        A shallow copy of ``auto_details`` with the allowed updates applied.

    Raises
    ------
    ValueError
        If any key in ``field_updates`` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If ``auto_details`` or ``field_updates`` is not a mapping.

    Notes
    -----
    This function performs a shallow copy of ``auto_details`` to avoid mutating the
    caller's data. It also validates that only whitelisted fields are modified,
    mitigating CWE-915 risks.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Validate that all requested updates are allowed
    disallowed = set(field_updates) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(f"Attempted to modify disallowed fields: {', '.join(disallowed)}")

    # Create a shallow copy to avoid side effects
    updated = copy.deepcopy(auto_details)

    for key, value in field_updates.items():
        # Only update if the key exists or is allowed to be added
        updated[key] = value

    return updated


# Example usage (commented out to keep the module importable without side effects)
# if __name__ == "__main__":
#     vehicle = {"make": "Toyota", "model": "Corolla", "year": 2018}
#     updates = {"color": "blue", "mileage": 25000, "unknown_field": "test"}
#     try:
#         new_vehicle = modify_auto_data(vehicle, updates)
#         print(new_vehicle)
#     except ValueError as e:
#         print(e)