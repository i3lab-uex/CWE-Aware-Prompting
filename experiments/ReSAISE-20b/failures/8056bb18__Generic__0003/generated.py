# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

This module provides a single function, `modify_vehicle_data`, which
updates an existing vehicle dictionary with new values for allowed fields.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Define the set of attributes that are allowed to be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
)

def modify_vehicle_data(vehicle_info: Dict[str, Any],
                        modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with new values for permitted fields.

    Parameters
    ----------
    vehicle_info : dict
        Dictionary representing a vehicle's current state.
    modifications : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    The function modifies ``vehicle_info`` in place and returns the same dictionary.
    """
    allowed_set = set(ALLOWED_FIELDS)

    for key, value in modifications.items():
        if key not in allowed_set:
            raise ValueError(f"Field '{key}' is not permitted for modification.")
        vehicle_info[key] = value

    return vehicle_info