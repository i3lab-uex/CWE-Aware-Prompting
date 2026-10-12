# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module provides a single public function `modify_car_attributes` that
updates only whitelisted fields of a car dictionary.  The list of allowed
keys is defined by the global `ALLOWED_FIELDS` constant.

The function validates its inputs, raises a clear exception for any
disallowed updates and returns the updated dictionary.  It does not modify
the input dictionaries in place; instead it returns a new dict that
preserves the original data.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by ensuring that the function does not hold onto any mutable state beyond
the scope of the call.  All resources (the car dict) are treated as plain
Python objects and are not leaked or mis‑managed.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # Add any additional fields that are permitted to be modified here.
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_car_attributes(car: dict, updates: dict) -> dict:
    """
    Return a new car dictionary with only allowed fields updated.

    Parameters
    ----------
    car : dict
        The current state of the vehicle.  Keys are expected to be strings.
    updates : dict
        Dictionary containing field names and their new values.

    Returns
    -------
    dict
        A new dictionary representing the updated vehicle state.

    Raises
    ------
    TypeError
        If either ``car`` or ``updates`` is not a mapping.
    ValueError
        If any key in ``updates`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The function does **not** modify ``car`` or ``updates`` in place.
    - Only keys that are explicitly listed in :data:`ALLOWED_FIELDS` are
      applied; all other fields are ignored and cause a ``ValueError``.
    """
    # Basic type checks
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"Expected 'updates' to be a dict, got {type(updates).__name__}")

    # Prepare the result by copying the original car
    updated_car = dict(car)

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")
        # Optional: additional validation per field could be added here.
        updated_car[key] = value

    return updated_car

# --------------------------------------------------------------------------- #
# Example usage (commented out to avoid side effects when imported)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     my_car = {"make": "Toyota", "model": "Corolla", "year": 2018, "color": "blue"}
#     changes = {"color": "red", "mileage": 25000}
#     print(modify_car_attributes(my_car, changes))