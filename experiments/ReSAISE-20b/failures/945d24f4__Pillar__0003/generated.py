# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle information safely.

The update logic is limited to a whitelist of fields defined in
`ALLOWED_FIELDS`.  Attempts to modify disallowed keys raise a
ValueError.  The function operates on a copy of the input dictionary to
avoid accidental mutation of caller data.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration:  list of fields that are permitted to be updated.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = {
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # Add any other fields that your application deems safe to update.
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def update_car_information(car_details: Dict[str, Any],
                           changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a car's details in a controlled manner.

    Parameters
    ----------
    car_details : dict
        Dictionary containing the current vehicle attributes.
    changes : dict
        Dictionary with keys representing fields to update and values
        representing the new data.

    Returns
    -------
    dict
        A new dictionary containing the updated car details.

    Raises
    ------
    ValueError
        If any key in `changes` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If `car_details` or `changes` is not a dictionary.
    """
    # Validate input types
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original
    updated = car_details.copy()

    for key, new_value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Optionally, you could add type validation per field here.
        updated[key] = new_value

    return updated