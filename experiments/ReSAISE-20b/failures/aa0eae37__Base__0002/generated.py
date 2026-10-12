# -*- coding: utf-8 -*-
"""
Vehicle data modification utility.

This module defines a single public function `modify_auto_data` that safely updates
vehicle details based on a dictionary of field updates.  Only fields listed in the
global ``ALLOWED_FIELDS`` constant may be modified; attempts to modify any other
field raise a ``ValueError``.  The function returns a new dictionary containing the
updated values, leaving the original ``auto_details`` untouched.

The implementation follows best practices for defensive programming and mitigates
CWE‑915 by strictly controlling which attributes may be modified.
"""

from __future__ import annotations

from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Global configuration: list of fields that are allowed to be modified
# --------------------------------------------------------------------------- #
ALLOWED_FIELDS: Iterable[str] = (
    "make",
    "model",
    "year",
    "color",
    "mileage",
    "vin",
)

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_auto_data(
    auto_details: Dict[str, Any], field_updates: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Return a new dictionary with updated vehicle details.

    Parameters
    ----------
    auto_details : dict
        The original vehicle data.  Keys represent vehicle attributes.
    field_updates : dict
        A mapping of fields to update with their new values.

    Returns
    -------
    dict
        A new dictionary containing the original data with the requested updates
        applied to allowed fields.

    Raises
    ------
    ValueError
        If any key in ``field_updates`` is not present in ``ALLOWED_FIELDS``.

    Notes
    -----
    * The function does **not** modify ``auto_details`` in place.
    * Field names are case-sensitive.
    * If a field appears in ``field_updates`` but is not present in
      ``auto_details``, it will be added to the resulting dictionary.
    """
    # Validate that all requested updates are permitted
    for field in field_updates:
        if field not in ALLOWED_FIELDS:
            raise ValueError(
                f"Field '{field}' is not allowed to be modified. "
                f"Allowed fields: {sorted(ALLOWED_FIELDS)}"
            )

    # Create a shallow copy to avoid mutating the input
    updated_details = dict(auto_details)

    # Apply allowed updates
    for field, value in field_updates.items():
        updated_details[field] = value

    return updated_details