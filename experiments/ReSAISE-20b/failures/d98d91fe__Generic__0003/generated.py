# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle dictionaries.

The global list `ALLOWED_FIELDS` defines which attributes of a car dictionary
can be modified. The function :func:`modify_car_details` applies only those
changes that are permitted and raises an exception for any disallowed key.
"""

from typing import Dict, Any

# Define the fields that are allowed to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",           # Vehicle Identification Number
    "engine_size",
    "horsepower",
    "transmission",
    "drivetrain",
    "fuel_type",
    "mileage",
]


def modify_car_details(car: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a car dictionary with the provided changes.

    Parameters
    ----------
    car : dict
        Dictionary representing a vehicle.
    changes : dict
        Dictionary mapping attribute names to new values.

    Returns
    -------
    dict
        The updated car dictionary.

    Raises
    ------
    TypeError
        If `car` or `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not present in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dictionary, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dictionary, got {type(changes).__name__}")

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        car[key] = value

    return car