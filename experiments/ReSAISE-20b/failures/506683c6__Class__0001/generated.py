# -*- coding: utf-8 -*-
"""
Utility module for safely updating vehicle attribute dictionaries.

The module exposes a single function, `modify_car_attributes`, which updates
only the keys listed in the global `ALLOWED_FIELDS` list.  Any attempt to
modify a disallowed key will raise a ``ValueError``.
"""

from __future__ import annotations

# List of keys that are allowed to be modified.  Extend this list as needed.
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
    Update a vehicle's attributes with the provided ``updates`` dictionary.

    Parameters
    ----------
    car : dict
        The current state of the vehicle.  This dictionary is mutated in place.
    updates : dict
        Mapping from attribute names to new values.

    Returns
    -------
    dict
        The same dictionary instance that was passed in, now updated.

    Raises
    ------
    ValueError
        If ``updates`` contains a key that is not present in :data:`ALLOWED_FIELDS`.
    TypeError
        If ``car`` or ``updates`` is not a dictionary.

    Notes
    -----
    - The function performs no type validation on the values themselves; it
      merely enforces that only whitelisted keys are modified.
    - This implementation is deliberately simple and does not attempt to
      deep‑copy nested structures, as the caller should provide a flat
      dictionary of vehicle attributes.
    """
    if not isinstance(car, dict):
        raise TypeError(f"Expected 'car' to be a dict, got {type(car).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"Expected 'updates' to be a dict, got {type(updates).__name__}")

    for key in updates:
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{key}' is not allowed to be updated.")

    # All keys are valid; perform the update.
    car.update(updates)
    return car