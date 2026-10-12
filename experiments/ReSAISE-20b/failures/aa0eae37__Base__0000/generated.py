# -*- coding: utf-8 -*-
"""
Utility module for safely updating vehicle details.

The function `modify_auto_data` ensures that only fields explicitly allowed
by the global list `ALLOWED_FIELDS` can be modified.  This mitigates the risk
described in CWE‑915 (Improperly Controlled Modification of Dynamically‑Determined
Object Attributes).

Author: ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any


# Global list of fields that are permitted to be modified.
ALLOWED_FIELDS = [
    "make",
    "model",
    "year",
    "color",
    "vin",
    # add other allowed fields here
]


def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update the given `auto_details` dictionary with values from
    `field_updates`, but only for keys that are present in
    :data:`ALLOWED_FIELDS`.

    Parameters
    ----------
    auto_details:
        Dictionary containing the current vehicle data.  It must be a mapping
        type (e.g., dict).  The dictionary is modified in place.
    field_updates:
        Dictionary containing the fields to update and their new values.

    Returns
    -------
    dict
        The same dictionary instance as `auto_details`, after applying the
        permitted updates.

    Raises
    ------
    TypeError
        If either argument is not a dictionary-like mapping.
    ValueError
        If `field_updates` contains any key that is not in ``ALLOWED_FIELDS``.
    """
    if not isinstance(auto_details, dict):
        raise TypeError(f"auto_details must be a dict; got {type(auto_details).__name__}")
    if not isinstance(field_updates, dict):
        raise TypeError(f"field_updates must be a dict; got {type(field_updates).__name__}")

    # Find any disallowed fields
    disallowed = [k for k in field_updates if k not in ALLOWED_FIELDS]
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(disallowed)}"
        )

    # Apply allowed updates
    auto_details.update(field_updates)

    return auto_details


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    vehicle = {"make": "Toyota", "model": "Corolla", "year": 2010}
    updates = {"color": "red", "year": 2021}

    try:
        updated_vehicle = modify_auto_data(vehicle, updates)
        print(updated_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")