# -*- coding: utf-8 -*-
"""
Vehicle data modification utilities.

This module defines a global list of fields that are allowed to be updated
in a vehicle dictionary. The `modify_vehicle_data` function updates only those
fields that are present in the allowed list and raises a ValueError if an
attempt is made to modify a disallowed field.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Allowed fields that can be updated in a vehicle dictionary
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
    "price",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_vehicle_data(
    vehicle_info: dict,
    modifications: dict,
) -> dict:
    """
    Update a vehicle dictionary with permitted fields.

    Parameters
    ----------
    vehicle_info : dict
        The original vehicle data.
    modifications : dict
        A mapping of field names to new values that should be applied.

    Returns
    -------
    dict
        The updated vehicle dictionary. The original `vehicle_info` is not
        modified in place.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The function performs a shallow copy of `vehicle_info` to avoid side‑effects.
    - Only keys listed in :data:`ALLOWED_FIELDS` are applied; others raise an error.
    - The function is deliberately simple to keep the API clear and secure.
    """
    # Defensive copy: ensure we don't modify the original dict
    updated_vehicle = vehicle_info.copy()

    for key, new_value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be modified. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        updated_vehicle[key] = new_value

    return updated_vehicle