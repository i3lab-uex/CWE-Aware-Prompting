# -*- coding: utf-8 -*-
"""
Vehicle information update utility.

This module provides a single public function :func:`update_car_information`
which safely updates the fields of a car detail dictionary.  Only keys listed
in :data:`ALLOWED_FIELDS` are permitted to be modified.

The implementation guards against CWE-915 by validating that the field names
provided in ``changes`` are explicitly allowed and that all inputs are of the
expected type.  Any attempt to modify a disallowed field raises a
``ValueError``.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration – allowed fields that can be updated
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "transmission",
    "fuel_type",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_car_information(car_details: dict, changes: dict) -> dict:
    """
    Update a car's details dictionary with the provided ``changes``.

    Parameters
    ----------
    car_details : dict
        The original dictionary containing the vehicle's details.  It is
        modified in place and also returned.
    changes : dict
        A dictionary mapping field names to new values that should be applied.

    Returns
    -------
    dict
        The updated ``car_details`` dictionary.

    Raises
    ------
    TypeError
        If either argument is not a ``dict``.
    ValueError
        If ``changes`` contains any key that is not in :data:`ALLOWED_FIELDS`.
    """

    # Validate argument types
    if not isinstance(car_details, dict):
        raise TypeError(f"car_details must be a dict, got {type(car_details).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict, got {type(changes).__name__}")

    # Iterate over the changes and apply only allowed fields
    for field, new_value in changes.items():
        if not isinstance(field, str):
            raise TypeError(f"Field names must be strings; got {type(field).__name__}")

        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not permitted for update.")

        # Perform the update
        car_details[field] = new_value

    return car_details


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    car = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2010,
        "color": "Blue",
    }

    changes = {
        "year": 2012,
        "color": "Red",
    }

    updated_car = update_car_information(car, changes)
    print(updated_car)  # {'make': 'Toyota', 'model': 'Corolla', 'year': 2012, 'color': 'Red'}