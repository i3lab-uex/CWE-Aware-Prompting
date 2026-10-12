# -*- coding: utf-8 -*-
"""
Utility module for updating vehicle information safely.

This module defines a global list `ALLOWED_FIELDS` which contains the
keys that are permitted to be modified in a vehicle's detail dictionary.
The function `update_car_information` applies changes only to those
keys and raises a ValueError if an attempt is made to modify a
disallowed field.

The implementation follows best practices for defensive programming,
avoiding unintended side effects and ensuring that the function
behaves predictably even when given unexpected input.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration: allowed keys that may be updated.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_car_information(car_details: dict, changes: dict) -> dict:
    """
    Update a vehicle's detail dictionary with the provided changes.

    Parameters
    ----------
    car_details : dict
        The original vehicle detail dictionary. It will be modified in place.
    changes : dict
        A mapping of fields to new values. Only keys present in
        ``ALLOWED_FIELDS`` will be applied.

    Returns
    -------
    dict
        The updated vehicle detail dictionary (same object as ``car_details``).

    Raises
    ------
    ValueError
        If any key in ``changes`` is not present in ``ALLOWED_FIELDS``.

    Notes
    -----
    - The function performs a shallow copy of the values from ``changes``.
      If nested mutable objects are present in ``car_details``, they will be
      referenced directly (no deep copy is performed).
    - The function modifies ``car_details`` in place for efficiency.
      If an immutable copy is required, the caller should create one
      before invoking this function.

    Example
    -------
    >>> car = {"make": "Toyota", "model": "Corolla", "year": 2010}
    >>> update_car_information(car, {"color": "red", "year": 2012})
    {'make': 'Toyota', 'model': 'Corolla', 'year': 2012, 'color': 'red'}
    """
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Validate that all requested changes are allowed
    invalid_keys = [k for k in changes if k not in ALLOWED_FIELDS]
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(invalid_keys)}"
        )

    # Apply the allowed changes
    for key, value in changes.items():
        car_details[key] = value

    return car_details