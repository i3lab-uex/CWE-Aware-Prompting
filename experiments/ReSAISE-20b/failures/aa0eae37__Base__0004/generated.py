# -*- coding: utf-8 -*-
"""
Vehicle data modifier.

This module provides a single function, `modify_auto_data`, which safely updates
fields of a vehicle dictionary. Only keys listed in the global `ALLOWED_FIELDS`
are permitted to be modified.

The implementation guards against improper dynamic attribute modification
(CWE-915) by performing explicit validation of the update keys before applying
them.  The original dictionary is not mutated; instead a new dictionary is
returned with the applied changes.
"""

from __future__ import annotations

# List of keys that may be updated.  Extend this list to allow more fields.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    # Add other permitted fields here
]

def modify_auto_data(
    auto_details: dict[str, any],
    field_updates: dict[str, any]
) -> dict[str, any]:
    """
    Return a new dictionary with allowed fields updated.

    Parameters
    ----------
    auto_details : dict[str, any]
        The original vehicle details.
    field_updates : dict[str, any]
        Proposed updates. Only keys in ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict[str, any]
        A new dictionary containing the original data with valid updates applied.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in ``field_updates`` is not permitted.

    Notes
    -----
    The function performs a shallow copy of the original dictionary to avoid
    side‑effects.  If you need deep copies for nested structures, adjust the
    implementation accordingly.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Validate that all requested updates are allowed
    invalid_keys = [k for k in field_updates if k not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(f"Attempted to update disallowed fields: {invalid_keys}")

    # Create a shallow copy and apply updates
    updated_details = auto_details.copy()
    updated_details.update(field_updates)

    return updated_details