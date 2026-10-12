# -*- coding: utf-8 -*-
"""
Utility to safely modify vehicle details.

The module exposes a single public function `modify_auto_data` that updates
fields of an automobile dictionary only if those fields are present in the
global `ALLOWED_FIELDS` list.  Attempts to modify disallowed keys raise a
``ValueError``.  The function performs basic type checks and returns a new
dictionary with the updates applied, leaving the original input untouched.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# List of field names that callers are allowed to modify.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    "mileage",
    "fuel_type",
    "transmission",
    "price",
]

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_auto_data(
    auto_details: dict,
    field_updates: dict
) -> dict:
    """
    Return a new dictionary with updates applied to `auto_details`.

    Parameters
    ----------
    auto_details : dict
        Original vehicle details. Must be a mapping of string keys to any values.
    field_updates : dict
        Mapping of fields to new values. Only keys present in ``ALLOWED_FIELDS``
        are applied; others cause a :class:`ValueError`.

    Returns
    -------
    dict
        A new dictionary containing the original details with updates applied.

    Raises
    ------
    TypeError
        If either argument is not a mapping.
    ValueError
        If any key in ``field_updates`` is not allowed.

    Notes
    -----
    The function does **not** modify ``auto_details`` in place.  This
    behaviour prevents accidental side‑effects and keeps the function pure.
    """
    # Validate inputs are mappings
    if not isinstance(auto_details, dict):
        raise TypeError(
            f"auto_details must be a dict; got {type(auto_details).__name__}"
        )
    if not isinstance(field_updates, dict):
        raise TypeError(
            f"field_updates must be a dict; got {type(field_updates).__name__}"
        )

    # Create a shallow copy to avoid mutating the original
    updated = auto_details.copy()

    for key, value in field_updates.items():
        if key not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{key}' is not allowed to be modified. "
                f"Allowed fields: {ALLOWED_FIELDS}"
            )
        updated[key] = value

    return updated