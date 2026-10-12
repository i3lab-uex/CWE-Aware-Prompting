# -*- coding: utf-8 -*-
"""
Vehicle attribute updater.

This module defines a single public function, `update_vehicle_attributes`,
which updates an automobile dictionary with new values while respecting
a list of fields that are allowed to be modified.  The implementation is
careful to avoid accidental mutation of the input dictionary and to raise
a clear exception if an attempt is made to modify a disallowed field.
"""

from __future__ import annotations

# List of fields that are permitted to be updated.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
]

def update_vehicle_attributes(automobile: dict, changes: dict) -> dict:
    """
    Return a new dictionary with the vehicle attributes updated according
    to `changes`. Only keys present in :data:`ALLOWED_FIELDS` are applied.
    If any key in `changes` is not allowed, a :class:`ValueError` is raised.

    Parameters
    ----------
    automobile:
        Current state of the vehicle as a dictionary.  The function does not
        modify this input; instead, it returns a new dictionary.
    changes:
        Dictionary containing keys and values to apply to the vehicle.

    Returns
    -------
    dict
        A new dictionary containing the updated attributes.

    Raises
    ------
    ValueError
        If `changes` contains a key that is not in :data:`ALLOWED_FIELDS`.

    Examples
    --------
    >>> vehicle = {"make": "Toyota", "model": "Camry", "year": 2018}
    >>> update_vehicle_attributes(vehicle, {"color": "red", "year": 2020})
    {'make': 'Toyota', 'model': 'Camry', 'year': 2020, 'color': 'red'}

    >>> update_vehicle_attributes(vehicle, {"owner": "Alice"})
    Traceback (most recent call last):
        ...
    ValueError: Attempt to modify disallowed field 'owner'
    """
    # Validate that all keys in `changes` are allowed
    disallowed = [key for key in changes if key not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempt to modify disallowed field(s): {', '.join(disallowed)}"
        )

    # Create a shallow copy of the original to avoid side effects
    updated = dict(automobile)

    # Apply allowed changes
    for key, value in changes.items():
        updated[key] = value

    return updated