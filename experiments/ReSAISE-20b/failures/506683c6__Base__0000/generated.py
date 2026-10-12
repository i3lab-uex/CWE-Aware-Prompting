# -*- coding: utf-8 -*-

"""
Module that provides a safe way to modify vehicle attributes.
"""

# Global list of fields that are allowed to be updated
ALLOWED_FIELDS = ["make", "model", "year", "color", "mileage"]

def modify_car_attributes(car: dict, updates: dict) -> dict:
    """
    Update a car dictionary with values from `updates`, but only for keys
    that are present in the global ALLOWED_FIELDS list.

    Parameters
    ----------
    car : dict
        Current state of the vehicle attributes.
    updates : dict
        Dictionary containing new values for some fields.

    Returns
    -------
    dict
        The updated car dictionary. The original `car` object is mutated and returned.

    Raises
    ------
    KeyError
        If `updates` contains a key that is not in ALLOWED_FIELDS.
    TypeError
        If either `car` or `updates` is not a dictionary.

    Notes
    -----
    This function protects against CWE-915 by strictly controlling which
    attributes can be modified. Any attempt to change disallowed fields will
    raise an exception, preventing accidental or malicious tampering.
    """
    if not isinstance(car, dict):
        raise TypeError("car must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Attempted to modify disallowed field: {key!r}")
        car[key] = value

    return car