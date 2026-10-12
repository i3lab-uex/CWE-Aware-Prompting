# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle data safely.
"""

from typing import Dict, Any

# Global list of fields that are permitted to be updated
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "price",
]

def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the provided `auto_details` dictionary with values from
    `field_updates`, but only for keys that are present in the global
    ``ALLOWED_FIELDS`` list.

    Parameters
    ----------
    auto_details : dict
        Dictionary containing the current vehicle details.
    field_updates : dict
        Dictionary of fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle details.
        The original ``auto_details`` is not modified.

    Raises
    ------
    ValueError
        If any key in ``field_updates`` is not present in ``ALLOWED_FIELDS``.
    """
    # Ensure we don't modify the original dictionary
    updated = auto_details.copy()

    for key, new_value in field_updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be updated. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        # Perform a shallow assignment; for complex types, further validation
        # may be required (e.g., ensuring ``new_value`` is of the correct type).
        updated[key] = new_value

    return updated