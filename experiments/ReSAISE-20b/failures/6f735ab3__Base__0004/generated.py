# -*- coding: utf-8 -*-
"""
Vehicle update utility.

The function `update_vehicle_info` updates only the attributes that are
explicitly allowed by the global ``ALLOWED_FIELDS`` list.  Any attempt to
modify a disallowed attribute will raise a ``ValueError``.

The implementation follows best practices for security and code quality:
* Only whitelisted attributes can be changed.
* The function does not mutate the input ``updates`` dictionary.
* A shallow copy of the vehicle is returned to avoid accidental side‑effects
  on external references.
"""

from __future__ import annotations

ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "owner",
    "registration",
]

def update_vehicle_info(vehicle: dict, updates: dict) -> dict:
    """
    Update a vehicle dictionary with allowed fields.

    Parameters
    ----------
    vehicle : dict
        Dictionary representing the vehicle object.  It may contain any keys,
        but only those listed in ``ALLOWED_FIELDS`` can be modified.
    updates : dict
        Dictionary containing the attributes to update.  Keys that are not in
        ``ALLOWED_FIELDS`` will cause a ``ValueError``.

    Returns
    -------
    dict
        A new dictionary with the updated values applied.

    Raises
    ------
    ValueError
        If ``updates`` contains a key that is not in ``ALLOWED_FIELDS``.
    TypeError
        If either argument is not a dictionary.

    Notes
    -----
    The function performs a shallow copy of ``vehicle`` before applying the
    updates, so callers retain their original dictionary unchanged.
    """
    if not isinstance(vehicle, dict):
        raise TypeError(f"vehicle must be a dict, got {type(vehicle).__name__}")
    if not isinstance(updates, dict):
        raise TypeError(f"updates must be a dict, got {type(updates).__name__}")

    # Create a shallow copy to avoid mutating the caller's dictionary
    updated_vehicle = vehicle.copy()

    for key, value in updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(f"Attempted to update disallowed field '{key}'")
        updated_vehicle[key] = value

    return updated_vehicle