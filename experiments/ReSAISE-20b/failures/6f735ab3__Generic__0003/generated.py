# SPDX-License-Identifier: MIT

"""
Utility module for updating vehicle information.
"""

from typing import Dict, Any, Iterable


# Global list of fields that can be updated
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "owner",
    "registration",
)


def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the attributes of a vehicle dictionary.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        Dictionary containing attribute names and new values.

    Returns
    -------
    dict
        A new dictionary with the updated vehicle data. The original `vehicle`
        dictionary is not modified.

    Raises
    ------
    ValueError
        If any key in `updates` is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If either argument is not a dictionary.
    """
    if not isinstance(vehicle, dict):
        raise TypeError("vehicle must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Copy the original vehicle to avoid mutating it
    updated_vehicle = dict(vehicle)

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        updated_vehicle[key] = value

    return updated_vehicle