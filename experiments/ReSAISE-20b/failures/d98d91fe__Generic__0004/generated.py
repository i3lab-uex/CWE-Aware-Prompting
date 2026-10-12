#!/usr/bin/env python3
"""
Vehicle details updater.

This module defines a single function `modify_car_details` that updates only
attributes of a vehicle dictionary which are listed in the global
`ALLOWED_FIELDS`.  Any attempt to modify an unauthorized field raises a
`ValueError`.

The function mutates the input dictionary and returns it for convenience.
"""

from __future__ import annotations

# List of attributes that are permitted to be modified
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "engine_type",
]

def modify_car_details(car: dict, changes: dict) -> dict:
    """
    Update a vehicle dictionary with permitted changes.

    Parameters
    ----------
    car : dict
        The original vehicle data.
    changes : dict
        Mapping of attribute names to new values.

    Returns
    -------
    dict
        The same dictionary instance, now updated with the allowed changes.

    Raises
    ------
    ValueError
        If `changes` contains a key that is not in `ALLOWED_FIELDS`.
    """
    # Ensure we only modify allowed fields
    disallowed = set(changes) - set(ALLOWED_FIELDS)
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Apply changes
    car.update(changes)
    return car


# Example usage (this block is executed only when running the module directly)
if __name__ == "__main__":
    sample_car = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2015,
        "color": "Blue",
        "vin": "JTDBR32E520123456",
        "mileage": 75000,
        "engine_type": "I4",
    }

    try:
        updated_car = modify_car_details(
            sample_car,
            {
                "color": "Red",
                "mileage": 80000,
                # "owner": "John Doe",   # Uncommenting this line would raise ValueError
            },
        )
        print("Updated car:", updated_car)
    except ValueError as exc:
        print(f"Error: {exc}")