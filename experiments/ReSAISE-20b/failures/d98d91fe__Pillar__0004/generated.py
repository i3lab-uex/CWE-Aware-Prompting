# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle dictionaries safely.
"""

from typing import Dict, Any

# Fields that are allowed to be modified
ALLOWED_FIELDS = {"make", "model", "year", "color", "mileage", "vin"}

def modify_car_details(car: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with the provided changes, but only for
    fields listed in ALLOWED_FIELDS.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.
    changes : dict
        Dictionary mapping attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary (same object as ``car``).

    Raises
    ------
    ValueError
        If a key in *changes* is not present in ALLOWED_FIELDS.
    TypeError
        If ``car`` or ``changes`` are not dictionaries.

    Notes
    -----
    The function performs a shallow update. It does not copy the original
    dictionary; modifications affect the input object directly.

    Security Considerations
    -----------------------
    - Only permitted fields can be altered, preventing accidental or malicious
      modification of critical data.
    - The function validates that the inputs are dictionaries to avoid type
      errors or unexpected behavior.
    """
    if not isinstance(car, dict):
        raise TypeError("`car` must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("`changes` must be a dictionary.")

    for key, value in changes.items():
        if not isinstance(key, str):
            raise TypeError(f"Field name must be a string, got {type(key).__name__}")
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be modified.")
        car[key] = value

    return car