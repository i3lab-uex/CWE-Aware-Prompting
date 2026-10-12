# -*- coding: utf-8 -*-
"""
Utility module for vehicle data manipulation.
"""

from copy import deepcopy
from typing import Dict, Any

# Fields that are permitted to be updated.
ALLOWED_FIELDS = {"make", "model", "year", "owner", "registration"}


def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with new attribute values.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data. Must be a mapping.
    updates : dict
        A dictionary of attributes to update. Keys must be in ALLOWED_FIELDS.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    TypeError
        If either `vehicle` or `updates` is not a mapping.
    ValueError
        If any key in `updates` is not allowed.

    Notes
    -----
    The function does **not** modify the original `vehicle` dictionary; it returns a new
    instance containing the merged data. This protects against unintended side effects and
    mitigates CWE-664 by ensuring that the lifetime of the original resource is not
    inadvertently altered.
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"vehicle must be a dict, got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict, got {type(updates).__name__}")

    # Validate update keys
    invalid_keys = set(updates) - ALLOWED_FIELDS
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {sorted(invalid_keys)}")

    # Create a shallow copy of the original vehicle to avoid mutation.
    updated_vehicle = deepcopy(vehicle)

    # Apply allowed updates
    for key, value in updates.items():
        updated_vehicle[key] = value

    return updated_vehicle