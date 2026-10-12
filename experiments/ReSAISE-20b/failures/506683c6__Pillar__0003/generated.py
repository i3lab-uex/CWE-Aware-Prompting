# -*- coding: utf-8 -*-

"""
Utility for updating vehicle dictionaries while enforcing a whitelist of
modifiable fields.
"""

from typing import Dict, Any

# Define which keys are allowed to be updated. Add or remove fields as needed.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    "mileage",
]

def modify_car_attributes(car: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with the vehicle attributes updated according
    to *updates*, but only for keys listed in :data:`ALLOWED_FIELDS`.

    Parameters
    ----------
    car :
        Current state of the vehicle as a dictionary.
    updates :
        Dictionary containing fields to update and their new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle attributes.

    Raises
    ------
    KeyError
        If *updates* contains a key that is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The original *car* dictionary is not modified.
    - This function performs a shallow copy; nested mutable values are shared
      between the original and returned dictionary.
    """
    # Create a shallow copy to avoid mutating the input
    updated_car = car.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified.")
        updated_car[key] = value

    return updated_car