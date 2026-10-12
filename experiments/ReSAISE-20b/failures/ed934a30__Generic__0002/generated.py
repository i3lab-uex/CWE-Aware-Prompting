# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

The module exposes a single public function `alter_vehicle_info` that
updates allowed vehicle fields in-place and returns the updated dictionary.
"""

from typing import Dict, Any

# Global list of fields that are permitted to be altered
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
]


def alter_vehicle_info(details: Dict[str, Any], modifications: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle's attributes with the provided modifications.

    Parameters
    ----------
    details : dict
        Current state of vehicle attributes. Keys represent attribute names.
    modifications : dict
        Proposed changes to the vehicle's attributes.

    Returns
    -------
    dict
        The updated `details` dictionary after applying valid modifications.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(details, dict):
        raise TypeError("`details` must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("`modifications` must be a dictionary")

    for key, new_value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        details[key] = new_value

    return details