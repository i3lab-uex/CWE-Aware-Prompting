# -*- coding: utf-8 -*-

from typing import Dict, Any

# Global list of fields that can be updated
ALLOWED_FIELDS = ["make", "model", "year", "owner", "registration"]


def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with the provided updates.

    Parameters
    ----------
    vehicle : dict
        Dictionary representing a vehicle. Must contain keys corresponding to vehicle attributes.
    updates : dict
        Dictionary containing attribute names as keys and new values.

    Returns
    -------
    dict
        A new dictionary with the updates applied. The original vehicle dict is not modified.

    Raises
    ------
    KeyError
        If an update key is not in the list of allowed fields.
    """
    if not isinstance(vehicle, dict):
        raise TypeError("vehicle must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Create a shallow copy to avoid mutating the original vehicle
    updated_vehicle = vehicle.copy()

    for field, new_value in updates.items():
        if field not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{field}' is not allowed to be updated.")
        # Optionally, you can add validation for specific fields here
        updated_vehicle[field] = new_value

    return updated_vehicle