# -*- coding: utf-8 -*-
"""
Vehicle information updater.

This module defines a function `adjust_vehicle_info` that safely updates
attributes of a vehicle dictionary. Only attributes listed in the global
``ALLOWED_FIELDS`` list may be modified. Any attempt to modify a
non‑permitted field results in a ``ValueError``.

The implementation follows best practices to mitigate CWE-915
(Improperly Controlled Modification of Dynamically‑Determined Object
Attributes).
"""

from __future__ import annotations

# Define the set of fields that are allowed to be modified.
ALLOWED_FIELDS = {
    "make",
    "model",
    "year",
    "color",
    "vin",
    "engine_type",
    "transmission",
    "body_style",
    # Add more allowed fields here as needed.
}


def adjust_vehicle_info(auto: dict, modifications: dict) -> dict:
    """
    Update a vehicle dictionary with new values for permitted fields.

    Parameters
    ----------
    auto : dict
        The vehicle dictionary to be updated. It is modified in place.
    modifications : dict
        A mapping of field names to new values. Only keys present in
        ``ALLOWED_FIELDS`` are applied.

    Returns
    -------
    dict
        The updated vehicle dictionary (the same object that was passed in).

    Raises
    ------
    ValueError
        If any key in ``modifications`` is not in ``ALLOWED_FIELDS``.

    Notes
    -----
    * The function modifies the original dictionary in place and returns it.
    * The check is performed before any mutation to ensure no partial
      updates occur if an invalid key is detected.
    """
    # Validate all requested modifications first.
    disallowed = [key for key in modifications if key not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Apply the permitted modifications.
    for key, value in modifications.items():
        auto[key] = value

    return auto