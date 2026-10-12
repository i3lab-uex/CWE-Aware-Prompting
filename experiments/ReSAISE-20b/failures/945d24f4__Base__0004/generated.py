#!/usr/bin/env python3
"""
Secure car information updater.

This module provides a single public function `update_car_information` that safely updates
attributes of a car dictionary only if those attributes are listed in the global
``ALLOWED_FIELDS``.  This prevents CWE‑915 style attacks where an attacker could inject
arbitrary keys to modify unintended attributes.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of fields that are allowed to be updated.  Modify this list as needed.
ALLOWED_FIELDS: Iterable[str] = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    # add additional allowed fields here
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def update_car_information(car_details: Dict[str, Any], changes: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with updated car information.

    Parameters
    ----------
    car_details : dict
        Original dictionary containing the vehicle's details.
    changes : dict
        Dictionary mapping field names to new values that should be applied.

    Returns
    -------
    dict
        A new dictionary containing the original fields plus any valid updates.

    Raises
    ------
    ValueError
        If `changes` contains a key that is not in ``ALLOWED_FIELDS``.
    TypeError
        If either `car_details` or `changes` is not a dictionary.

    Notes
    -----
    - The function performs a shallow copy of ``car_details``; nested mutable objects
      are not deeply copied.
    - The original `car_details` dictionary is left untouched to avoid side effects.

    Example
    -------
    >>> car = {"make": "Toyota", "model": "Camry", "year": 2018}
    >>> update_car_information(car, {"color": "red", "mileage": 12000})
    {'make': 'Toyota', 'model': 'Camry', 'year': 2018, 'color': 'red', 'mileage': 12000}
    """
    if not isinstance(car_details, dict):
        raise TypeError(f"car_details must be a dict; got {type(car_details).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict; got {type(changes).__name__}")

    # Verify that all requested changes are allowed
    disallowed = [key for key in changes if key not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"The following fields are not allowed to be updated: {', '.join(disallowed)}"
        )

    # Create a copy so the original is not mutated
    updated = copy.copy(car_details)

    # Apply changes
    for key, value in changes.items():
        updated[key] = value

    return updated