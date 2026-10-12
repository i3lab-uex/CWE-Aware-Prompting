# -*- coding: utf-8 -*-
"""
Vehicle update utility.

This module defines a single public function, :func:`update_vehicle_info`, which
updates the attributes of a vehicle dictionary based on an ``updates`` mapping.
Only fields listed in :data:`ALLOWED_FIELDS` are permitted to be modified.  Any
attempt to modify disallowed fields will raise a :class:`ValueError`.

The implementation avoids executing arbitrary code by performing only
dictionary operations and simple type checks.  No external resources are
accessed, mitigating CWE‑913 concerns.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]


def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Update a vehicle dictionary with the provided ``updates``.

    Parameters
    ----------
    vehicle : dict
        The original vehicle dictionary.  It is modified in place.
    updates : dict
        Mapping of field names to new values.  Only keys present in
        :data:`ALLOWED_FIELDS` are applied.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object as ``vehicle``).

    Raises
    ------
    TypeError
        If either ``vehicle`` or ``updates`` is not a dictionary.
    ValueError
        If an attempt is made to update a field that is not in
        :data:`ALLOWED_FIELDS`.

    Notes
    -----
    - The function performs a shallow update; nested structures are not deep‑copied.
    - No execution of code from the input is performed, preventing
      CWE‑913 vulnerabilities.

    Examples
    --------
    >>> v = {"make": "Ford", "model": "F-150", "year": 2018, "owner": "Alice"}
    >>> update_vehicle_info(v, {"model": "F-150 Raptor", "year": 2020})
    {'make': 'Ford', 'model': 'F-150 Raptor', 'year': 2020, 'owner': 'Alice'}
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"vehicle must be a dict, got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict, got {type(updates).__name__}")

    for field, new_value in updates.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(f"Field '{field}' is not allowed to be updated")
        # Optional: Validate that the field exists in vehicle
        if field not in vehicle:
            raise KeyError(f"Field '{field}' does not exist in the vehicle object")
        vehicle[field] = new_value

    return vehicle