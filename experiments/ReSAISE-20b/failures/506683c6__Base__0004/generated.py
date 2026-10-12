# -*- coding: utf-8 -*-
"""
Utility for safely updating vehicle attributes.

The module exposes a single public function, :func:`modify_car_attributes`, that
updates only fields listed in the global ``ALLOWED_FIELDS`` list.  Any attempt to
modify a field not present in this whitelist will raise a ``KeyError``.
"""

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
]

def modify_car_attributes(car: dict, updates: dict) -> dict:
    """
    Update allowed fields of a car dictionary.

    Parameters
    ----------
    car : dict
        Current state of vehicle attributes.
    updates : dict
        Desired changes to the car's attributes.

    Returns
    -------
    dict
        The updated car dictionary.

    Raises
    ------
    KeyError
        If ``updates`` contains a key that is not in :data:`ALLOWED_FIELDS`.
    TypeError
        If ``car`` or ``updates`` is not a mapping.
    """
    if not isinstance(car, dict):
        raise TypeError(f"'car' must be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"'updates' must be a dict, got {type(updates).__name__}")

    # Create a shallow copy to avoid mutating the original
    updated_car = car.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise KeyError(f"Field '{key}' is not allowed to be modified.")
        updated_car[key] = value

    return updated_car