# -*- coding: utf-8 -*-

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
    "transmission",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update a car dictionary with new values for permitted fields.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.  It is modified in place.
    changes : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        The updated car dictionary.

    Raises
    ------
    TypeError
        If `car` or `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not present in ALLOWED_FIELDS.
    """
    if not isinstance(car, dict):
        raise TypeError("`car` must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary")

    for field, new_value in changes.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be modified.")
        car[field] = new_value

    return car