# -*- coding: utf-8 -*-

"""
Vehicle attribute updater.

This module defines a single public function, `alter_vehicle_info`, that
updates an existing vehicle dictionary with new values.  Only a predefined set
of keys (specified by the global `ALLOWED_FIELDS` list) may be modified.
Attempting to change any other key will raise a ValueError.

The implementation is intentionally defensive: it validates input types,
creates a shallow copy of the original dictionary before applying changes
to avoid accidental mutation, and documents behaviour clearly.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration:  Which fields are allowed to be modified
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Update the vehicle dictionary with new values.

    Parameters
    ----------
    details : dict
        The current state of the vehicle.  Must be a mapping.
    modifications : dict
        Mapping containing keys and new values to apply.

    Returns
    -------
    dict
        A new dictionary that contains the updated vehicle data.
        The original `details` dictionary is not modified.

    Raises
    ------
    TypeError
        If either `details` or `modifications` is not a dictionary.
    ValueError
        If any key in `modifications` is not present in :data:`ALLOWED_FIELDS`.
    """
    # Basic type checks
    if not isinstance(details, dict):
        raise TypeError(f"'details' must be a dict, got {type(details).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"'modifications' must be a dict, got {type(modifications).__name__}")

    # Create a copy so the caller's data is not mutated
    updated = dict(details)

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Attempted to modify disallowed field '{key}'. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        updated[key] = value

    return updated