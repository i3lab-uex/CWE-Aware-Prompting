#!/usr/bin/env python3
"""
Utility to safely alter employee records.

This module defines a single public function `alter_employee_details`
that applies validated changes to an employee dictionary.  Non‑admin
users may only modify attributes listed in the global `EDITABLE_FIELDS`
constant.  Admin users (``is_superuser=True``) are allowed to modify any
field, but all supplied keys must still exist in the employee record.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that normal users are permitted to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add more fields here if they become editable by non‑admin users.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary reflecting valid changes.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Desired modifications; keys are field names, values are new data.
    is_superuser : bool
        Flag indicating whether the updater has administrative privileges.

    Returns
    -------
    dict
        A shallow copy of ``emp_data`` with the requested modifications applied.

    Raises
    ------
    ValueError
        If a change attempts to modify a non‑editable field (for normal users)
        or if a supplied key does not exist in ``emp_data``.
    TypeError
        If either argument is not a mapping type.

    Notes
    -----
    * The function performs a shallow copy; nested mutable objects are shared.
    * No changes are made to the original ``emp_data`` dictionary.

    Security
    --------
    * The function guards against CWE‑915 by strictly validating the keys in
      ``changes`` before applying them.
    * Admin users can modify any field present in the record, but cannot
      introduce new keys that do not already exist.
    """
    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Prepare the updated record
    updated = emp_data.copy()

    for key, value in changes.items():
        # Key must exist in the original record
        if key not in emp_data:
            raise ValueError(f"Field '{key}' does not exist in employee data")

        # Non‑admin users are limited to EDITABLE_FIELDS
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"User lacks permission to modify field '{key}'. "
                "Only the following fields are editable: "
                f"{sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated[key] = value

    return updated


__all__ = ["alter_employee_details", "EDITABLE_FIELDS"]