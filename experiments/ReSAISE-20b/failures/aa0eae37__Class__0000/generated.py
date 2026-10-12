#!/usr/bin/env python3
"""
Utility module for safely updating vehicle details.

The function `modify_auto_data` updates only the fields that are explicitly
listed in the global ``ALLOWED_FIELDS`` list.  Any attempt to modify a field
outside this whitelist raises a :class:`ValueError`.  This design protects
against accidental or malicious modification of internal state, addressing
CWE‑913 concerns about uncontrolled dynamic code resource manipulation.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# --------------------------------------------------------------------------- #
# Global configuration: list of fields that may be updated
ALLOWED_FIELDS: List[str] = [
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",  # Vehicle Identification Number
]

# --------------------------------------------------------------------------- #
def modify_auto_data(auto_details: Dict[str, Any],
                     field_updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a new dictionary with updates applied to *auto_details*.

    Parameters
    ----------
    auto_details : dict
        The original vehicle details.  Keys are expected to be strings.
    field_updates : dict
        Mapping of fields to new values.  Only keys present in
        ``ALLOWED_FIELDS`` are applied; others raise :class:`ValueError`.

    Returns
    -------
    dict
        A shallow copy of *auto_details* with the allowed updates applied.

    Raises
    ------
    ValueError
        If *field_updates* contains a key not in ``ALLOWED_FIELDS``.
    TypeError
        If *auto_details* or *field_updates* is not a dictionary.
    """

    # Basic type checks
    if not isinstance(auto_details, dict):
        raise TypeError("auto_details must be a dictionary")
    if not isinstance(field_updates, dict):
        raise TypeError("field_updates must be a dictionary")

    # Make a shallow copy to avoid mutating the original input
    updated_details = copy.copy(auto_details)

    for field, new_value in field_updates.items():
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Attempted to modify disallowed field '{field}'. "
                "Only the following fields may be updated: "
                f"{', '.join(ALLOWED_FIELDS)}."
            )
        # Perform the update
        updated_details[field] = new_value

    return updated_details

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    vehicle = {
        "make": "Toyota",
        "model": "Corolla",
        "year": 2010,
        "color": "red",
        "mileage": 120000,
        "vin": "1234ABCDEF",
    }

    updates = {"color": "blue", "mileage": 118000}
    try:
        new_vehicle = modify_auto_data(vehicle, updates)
        print("Updated vehicle:", new_vehicle)
    except Exception as exc:
        print(f"Error: {exc}")