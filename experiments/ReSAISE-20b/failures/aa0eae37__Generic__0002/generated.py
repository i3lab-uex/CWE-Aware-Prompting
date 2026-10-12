# -*- coding: utf-8 -*-
"""
Utility for updating vehicle data with a whitelist of allowed fields.
"""

from typing import Dict, Any

# Global list of fields that can be safely modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    # Add more fields as needed
]


def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update vehicle details only for fields listed in ``ALLOWED_FIELDS``.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle information.
    field_updates : dict
        Dictionary with keys as fields to update and values as the new data.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object as ``auto_details``).

    Raises
    ------
    KeyError
        If any key in *field_updates* is not present in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    - The function mutates ``auto_details`` in place and returns it for convenience.
    - Only keys that are explicitly allowed will be updated; others raise an error to
      prevent accidental data corruption.
    """
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    for key, value in field_updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be updated.")
        auto_details[key] = value

    return auto_details