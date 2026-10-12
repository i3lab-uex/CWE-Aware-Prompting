# -*- coding: utf-8 -*-

"""
Vehicle Information Update Module

This module provides a single public function, `update_car_information`,
which safely updates only the fields that are explicitly permitted.
The list of allowed keys is defined by the global variable `ALLOWED_FIELDS`.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by ensuring that the function does not inadvertently create or delete
resources beyond what is required for the update operation.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable


# --------------------------------------------------------------------------- #
# Configuration: define which keys are allowed to be updated.
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "vin",          # Vehicle Identification Number
    "mileage",
    "engine_size",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_car_information(
    car_details: Dict[str, Any],
    changes: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary representing the vehicle's details after applying
    the specified changes. Only keys listed in `ALLOWED_FIELDS` are updated;
    all other keys are ignored.

    Parameters
    ----------
    car_details : dict
        Original dictionary containing the vehicle's current attributes.
    changes : dict
        Dictionary with keys to be updated and their new values.

    Returns
    -------
    dict
        A shallow copy of `car_details` with the allowed updates applied.

    Raises
    ------
    TypeError
        If either argument is not a dictionary.
    ValueError
        If `changes` contains keys that are not present in `ALLOWED_FIELDS`.
    """
    # Validate input types
    if not isinstance(car_details, dict):
        raise TypeError("car_details must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Filter changes to only those that are allowed
    filtered_changes = {
        key: value for key, value in changes.items()
        if key in ALLOWED_FIELDS
    }

    # Detect disallowed keys to provide a clear error message
    disallowed_keys = set(changes) - set(filtered_changes)
    if disallowed_keys:
        raise ValueError(
            f"The following fields are not allowed to be updated: "
            f"{', '.join(sorted(disallowed_keys))}"
        )

    # Create a shallow copy to avoid mutating the original dictionary
    updated = copy.copy(car_details)

    # Apply allowed changes
    for key, value in filtered_changes.items():
        updated[key] = value

    return updated