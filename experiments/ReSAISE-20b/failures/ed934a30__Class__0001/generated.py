# -*- coding: utf-8 -*-
"""
Vehicle modification utility.

This module provides a single public function :func:`alter_vehicle_info`
that updates vehicle attributes in a controlled manner.

The list ``ALLOWED_FIELDS`` defines which keys may be changed.  Any attempt
to modify a key not present in that list will raise :class:`ValueError`.

The function performs a shallow copy of the input dictionary before
applying modifications, so that callers retain their original data.
"""

from __future__ import annotations

# List of keys that are allowed to be updated.  Add or remove entries
# here to change the behaviour of :func:`alter_vehicle_info`.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "registration_number",
]

def alter_vehicle_info(details: dict, modifications: dict) -> dict:
    """
    Return a new dictionary containing the vehicle details with
    modifications applied, but only for keys that are listed in
    :data:`ALLOWED_FIELDS`.

    Parameters
    ----------
    details :
        A dictionary representing the current state of a vehicle.
    modifications :
        A dictionary containing key/value pairs to apply as updates.

    Returns
    -------
    dict
        A new dictionary with the requested changes applied.

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not present in
        :data:`ALLOWED_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of ``details``.  Nested objects are
    not deep‑copied; if you need that behaviour, use :func:`copy.deepcopy`
    before calling this function.

    Example
    -------
    >>> vehicle = {"make": "Toyota", "model": "Corolla", "year": 2010}
    >>> changes = {"color": "red", "year": 2012, "owner": "Alice"}
    >>> alter_vehicle_info(vehicle, changes)
    Traceback (most recent call last):
        ...
    ValueError: Modification of field 'owner' is not allowed
    """
    # Create a shallow copy to avoid mutating the caller's data.
    updated = dict(details)

    for key, value in modifications.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Modification of field '{key}' is not allowed")

        updated[key] = value

    return updated