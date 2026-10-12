# SPDX-License-Identifier: MIT

"""
Utility module for safely updating vehicle data dictionaries.

This module defines a list of attributes that are allowed to be modified
(`ALLOWED_FIELDS`) and provides the `modify_vehicle_data` function which
applies updates only to those permitted keys.  Any attempt to modify a
disallowed attribute will raise a `ValueError`, preventing unintended or
malicious changes to the vehicle data.

The implementation follows best practices for input validation and
immutability: it does not modify the original `vehicle_info` dictionary
in place, but instead returns a new dictionary containing the updates.
"""

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
]

def modify_vehicle_data(
    vehicle_info: dict,
    modifications: dict
) -> dict:
    """
    Return a new dictionary with the vehicle information updated according to
    `modifications`, but only for keys listed in ALLOWED_FIELDS.

    Parameters
    ----------
    vehicle_info : dict
        Original dictionary representing a vehicle.
    modifications : dict
        Dictionary containing attribute names as keys and new values to apply.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If any key in `modifications` is not present in ALLOWED_FIELDS.
    TypeError
        If either argument is not a dictionary.

    Examples
    --------
    >>> vehicle = {"make": "Toyota", "model": "Corolla", "year": 2015}
    >>> update = {"color": "blue", "mileage": 50000}
    >>> modify_vehicle_data(vehicle, update)
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2015, 'color': 'blue', 'mileage': 50000}
    """
    if not isinstance(vehicle_info, dict):
        raise TypeError("vehicle_info must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Validate keys
    disallowed = set(modifications) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Create a shallow copy to avoid mutating the original
    updated_vehicle = vehicle_info.copy()
    updated_vehicle.update(modifications)
    return updated_vehicle