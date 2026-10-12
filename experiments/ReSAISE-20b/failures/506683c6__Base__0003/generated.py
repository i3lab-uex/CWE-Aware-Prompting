# modify_car_attributes.py

"""
A utility to safely update vehicle attributes.

The function `modify_car_attributes` accepts a current car dictionary and an
updates dictionary.  Only keys listed in the global `ALLOWED_FIELDS` list are
applied; any other key will raise a ValueError.  The original car dictionary
is not mutated – a new dictionary containing the updated values is returned.

This design mitigates CWE‑915 (Improperly Controlled Modification of
Dynamically-Determined Object Attributes) by strictly whitelisting the fields
that can be altered.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable


# Global whitelist of attributes that may be modified.
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "mileage",
    "engine_type",
)


def _validate_inputs(car: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """
    Validate that `car` and `updates` are dictionaries and that all keys in
    `updates` are permitted.  Raises ValueError if any check fails.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected car to be a dict, got {type(car).__name__}")

    if not isinstance(updates, dict):
        raise TypeError(f"Expected updates to be a dict, got {type(updates).__name__}")

    disallowed = set(updates) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {sorted(disallowed)}"
        )


def modify_car_attributes(car: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary containing the original car data with any
    permitted updates applied.

    Parameters
    ----------
    car : dict
        Current state of the vehicle's attributes.
    updates : dict
        Mapping of fields to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary with the updates applied.

    Raises
    ------
    TypeError
        If `car` or `updates` is not a dictionary.
    ValueError
        If any key in `updates` is not listed in `ALLOWED_FIELDS`.
    """
    _validate_inputs(car, updates)

    # Create a shallow copy to avoid mutating the original dictionary.
    updated_car = car.copy()

    # Apply only allowed updates.
    for key, value in updates.items():
        updated_car[key] = value

    return updated_car


# Example usage (commented out – remove for production)
if __name__ == "__main__":
    sample_car = {
        "make": "Toyota",
        "model": "Camry",
        "year": 2020,
        "color": "Red",
        "vin": "1HGCM82633A004352",
        "mileage": 15000,
    }

    changes = {
        "color": "Blue",
        "mileage": 15200,
    }

    try:
        new_car = modify_car_attributes(sample_car, changes)
        print("Updated car:", new_car)
    except Exception as e:
        print(f"Error: {e}")