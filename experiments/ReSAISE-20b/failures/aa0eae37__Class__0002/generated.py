# -*- coding: utf-8 -*-
"""
Vehicle data modification module.

This module provides a single public function, `modify_auto_data`, which
updates an existing vehicle details dictionary with new values for a
subset of allowed fields. The function is defensive: it validates input
types, checks that only permitted keys are modified, and returns a new
dictionary so that the original data is not mutated.
"""

from __future__ import annotations

# List of fields that are allowed to be modified.  This should be kept in sync
# with the business rules of the application.
ALLOWED_FIELDS = ["make", "model", "year", "color", "vin"]

def modify_auto_data(
    auto_details: dict,
    field_updates: dict
) -> dict:
    """
    Apply updates to a vehicle's details dictionary.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle data.  Keys are expected to be
        strings and values can be of any JSON‑serialisable type.
    field_updates : dict
        Dictionary containing key/value pairs to be applied to `auto_details`.
        Only keys present in :data:`ALLOWED_FIELDS` will be accepted.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.  The original
        `auto_details` dictionary is left untouched.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `field_updates` contains keys that are not in :data:`ALLOWED_FIELDS`.
    """

    # Validate input types
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Ensure all update keys are allowed
    invalid_keys = set(field_updates) - set(ALLOWED_FIELDS)
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {sorted(invalid_keys)}")

    # Create a shallow copy of the original data to avoid side‑effects
    updated_details = auto_details.copy()

    # Apply updates
    for key, value in field_updates.items():
        updated_details[key] = value

    return updated_details