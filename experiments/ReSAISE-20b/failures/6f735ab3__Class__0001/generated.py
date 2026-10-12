# -*- coding: utf-8 -*-
"""
Vehicle information updater.

This module defines a single public function, ``update_vehicle_info``, which
updates a vehicle dictionary with new values while strictly limiting the
attributes that may be modified.  The list of modifiable keys is defined in
the global ``ALLOWED_FIELDS`` variable.

The implementation follows the CWE‑913 guidance by ensuring that only
whitelisted attributes are written to the vehicle dictionary, preventing
arbitrary or malicious updates of hidden/internal fields.
"""

from __future__ import annotations

from typing import Dict, Any, Mapping, MutableMapping


# List of attributes that may be updated.  Add or remove keys as needed.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

def update_vehicle_info(
    vehicle: Mapping[str, Any],
    updates: Mapping[str, Any]
) -> Dict[str, Any]:
    """
    Return a new vehicle dictionary updated with values from ``updates``.

    Parameters
    ----------
    vehicle:
        A mapping representing the current state of a vehicle.  It must be
        dictionary-like and contain string keys.
    updates:
        A mapping of attribute names to new values.  Only attributes listed
        in :data:`ALLOWED_FIELDS` are applied; others are ignored.

    Returns
    -------
    dict
        A new dictionary containing the merged data.  The original ``vehicle``
        mapping is left untouched.

    Raises
    ------
    TypeError
        If ``vehicle`` or ``updates`` are not mapping types, or if any key is
        not a string.
    """
    # Validate input types
    if not isinstance(vehicle, Mapping):
        raise TypeError("vehicle must be a mapping type (e.g., dict)")
    if not isinstance(updates, Mapping):
        raise TypeError("updates must be a mapping type (e.g., dict)")

    # Ensure all keys are strings
    for key in vehicle:
        if not isinstance(key, str):
            raise TypeError(f"vehicle contains a non-string key: {key!r}")
    for key in updates:
        if not isinstance(key, str):
            raise TypeError(f"updates contains a non-string key: {key!r}")

    # Create a shallow copy to avoid mutating the original vehicle
    updated_vehicle: MutableMapping[str, Any] = dict(vehicle)

    # Apply only allowed updates
    for key in ALLOWED_FIELDS:
        if key in updates:
            updated_vehicle[key] = updates[key]

    return dict(updated_vehicle)