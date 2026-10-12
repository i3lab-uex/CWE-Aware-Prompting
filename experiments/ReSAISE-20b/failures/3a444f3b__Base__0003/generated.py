#!/usr/bin/env python3
"""
Secure employee record editing module.

The core function `edit_personnel_info` updates an employee dictionary
while enforcing strict field‑level permissions.  Non‑admin users may only
modify a predefined set of fields (`EDITABLE_FIELDS`).  Admins can modify
any existing field but cannot introduce new keys unless they already exist
in the original record.  This guards against CWE‑915: Improperly Controlled
Modification of Dynamically-Determined Object Attributes.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Fields that regular users are allowed to edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

def _validate_fields(
    original: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> None:
    """
    Validate that the requested updates are permitted.

    Raises:
        ValueError: If a non‑admin tries to modify a protected field or
                    if an admin attempts to add a brand new key.
    """
    for key in adjustments:
        # Disallow modifications of protected keys by non‑admin users.
        if not admin_flag and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

        # Admins may only update keys that already exist in the original record.
        if admin_flag and key not in original:
            raise ValueError(
                f"Admin cannot add new field '{key}' that does not exist in the record."
            )


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Update an employee's record with the provided adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key‑value pairs indicating fields to update and their new values.
    admin_flag : bool
        ``True`` if the updater has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a user attempts to modify disallowed fields or add new keys.
    """
    # Defensive copy to avoid mutating the caller's data
    updated = copy.deepcopy(employee_record)

    # Ensure adjustments is a dictionary
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")

    # Validate permissions
    _validate_fields(employee_record, adjustments, admin_flag)

    # Apply the permitted updates
    for key, value in adjustments.items():
        updated[key] = value

    return updated


# Example usage (for testing only, remove or guard under __main__ in production)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change salary (should raise ValueError)
    try:
        edit_personnel_info(employee, {"salary": 90000}, admin_flag=False)
    except ValueError as exc:
        print(f"Permission error: {exc}")

    # Admin changing salary and department
    updated_emp = edit_personnel_info(employee, {"salary": 90000, "department": "Engineering"}, admin_flag=True)
    print(updated_emp)