# update_vehicle_info.py

"""
Update vehicle attributes safely.

The function `update_vehicle_info` receives a dictionary representing a vehicle
and another dictionary containing the fields to update. Only attributes listed
in `ALLOWED_FIELDS` are permitted to be modified.

Security considerations:
* Input types are validated.
* Only whitelisted fields may be updated – attempting to modify a non‑allowed
  field raises `ValueError`.
* A shallow copy of the vehicle dictionary is returned, leaving the original
  unchanged (prevents accidental side effects).
"""

from typing import Dict, Any

# Global whitelist of fields that can be modified
ALLOWED_FIELDS = ["make", "model", "year", "owner", "registration"]


def update_vehicle_info(vehicle: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary with specified fields updated.

    Parameters
    ----------
    vehicle : dict
        The original vehicle data.
    updates : dict
        Fields to update with their new values.

    Returns
    -------
    dict
        A copy of `vehicle` with the updates applied.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If any key in `updates` is not in `ALLOWED_FIELDS`.
    """
    if not isinstance(vehicle, dict):
        raise TypeError("`vehicle` must be a dictionary.")
    if not isinstance(updates, dict):
        raise TypeError("`updates` must be a dictionary.")

    # Validate that all update keys are allowed
    for key in updates:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")

    # Create a shallow copy to avoid mutating the original
    updated_vehicle = vehicle.copy()

    # Apply updates
    for key, value in updates.items():
        updated_vehicle[key] = value

    return updated_vehicle