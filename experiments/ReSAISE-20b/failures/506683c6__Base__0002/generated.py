# -*- coding: utf-8 -*-
"""
Vehicle attribute modification utility.

This module defines a single function, `modify_car_attributes`, which
updates a vehicle dictionary with new values for a subset of fields.
Only keys listed in the global `ALLOWED_FIELDS` are permitted to be
modified. Any attempt to modify a disallowed key results in a
``ValueError`` exception.

The implementation is intentionally defensive:
* The function works on a shallow copy of the input dictionary to
  avoid mutating callers' data unexpectedly.
* It performs a strict membership test against the allowed fields
  to guard against accidental or malicious attribute injection.
"""

from typing import Dict, Any

# Global list of fields that may be modified.  Add or remove keys as
# required by the application policy.
ALLOWED_FIELDS = {"make", "model", "year", "color", "vin"}

def modify_car_attributes(car: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update a vehicle dictionary with new values for allowed fields.

    Parameters
    ----------
    car : dict
        The original vehicle dictionary. Keys should be strings.
    updates : dict
        A mapping of field names to new values.

    Returns
    -------
    dict
        A new dictionary containing the updated vehicle data.

    Raises
    ------
    ValueError
        If any key in ``updates`` is not present in :data:`ALLOWED_FIELDS`.

    Notes
    -----
    The function does **not** modify the input ``car`` dictionary in place.
    It returns a new dictionary that merges the original data with the
    provided updates for allowed fields only.
    """
    # Validate that all update keys are permitted
    disallowed = set(updates) - ALLOWED_FIELDS
    if disallowed:
        raise ValueError(
            f"Attempted to modify disallowed fields: {', '.join(sorted(disallowed))}"
        )

    # Create a shallow copy to avoid side‑effects
    updated_car = car.copy()

    # Apply allowed updates
    for key, value in updates.items():
        updated_car[key] = value

    return updated_car