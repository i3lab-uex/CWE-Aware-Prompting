# -*- coding: utf-8 -*-
"""
Vehicle detail modification module.

The function `modify_car_details` updates only attributes that are explicitly
allowed.  All other attempts to modify the dictionary are ignored, preventing
unintended side effects or security issues related to CWE‑913.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Allowed fields that may be updated on a vehicle dictionary.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
    "engine",
]

# --------------------------------------------------------------------------- #
def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update permitted attributes of a vehicle dictionary.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary.  It is modified in place and also
        returned for convenience.
    changes : dict
        A mapping of attribute names to new values.

    Returns
    -------
    dict
        The updated vehicle dictionary.

    Raises
    ------
    TypeError
        If either `car` or `changes` is not a dictionary.
    ValueError
        If any key in `changes` is not listed in :data:`ALLOWED_FIELDS`.
    """
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dict, got {type(car).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"'changes' must be a dict, got {type(changes).__name__}")

    for key, value in changes.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to modify disallowed field '{key}'")
        # Basic type checks can be added here if desired
        car[key] = value

    return car


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "color": "red",
    }

    updates = {"color": "blue", "mileage": 50000}
    try:
        updated_vehicle = modify_car_details(vehicle, updates)
        print(updated_vehicle)
    except Exception as e:
        print(f"Error: {e}")