#!/usr/bin/env python3
"""
Employee record modification utility.

The module provides a single function `modify_staff_info` which applies
changes to an employee dictionary while enforcing access control.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration: fields that can be edited by non‑admin users.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _validate_field_change(field: str, admin_status: bool) -> None:
    """
    Raise a ValueError if the field is not allowed to be edited
    by the caller.

    Parameters
    ----------
    field : str
        The name of the field being changed.
    admin_status : bool
        Flag indicating whether the caller has administrative rights.

    Raises
    ------
    ValueError
        If a non‑admin attempts to edit a restricted field.
    """
    if not admin_status:
        if field == "social_security_number":
            raise ValueError("Non‑admin users cannot modify SSN.")
        if field not in EDITABLE_FIELDS:
            raise ValueError(f"Field '{field}' is not editable by non‑admin users.")


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Apply a set of changes to an employee record while enforcing
    edit permissions.

    Parameters
    ----------
    staff : dict
        Current employee record. Must contain keys for all standard
        attributes such as 'name', 'position', 'salary',
        'department' and optionally 'social_security_number'.
    changes : dict
        Dictionary of fields to update with their new values.
    admin_status : bool
        ``True`` if the caller has administrative privileges,
        otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a restricted field.

    Notes
    -----
    - The original ``staff`` dictionary is **not** mutated.
    - Only keys present in the original record are updated; new keys
      are ignored to prevent accidental schema drift.
    """
    # Defensive copy: do not alter the caller's dictionary
    updated_staff = copy.deepcopy(staff)

    for field, new_value in changes.items():
        # Ignore attempts to add completely unknown fields
        if field not in updated_staff:
            continue

        # Enforce permission checks
        _validate_field_change(field, admin_status)

        # Apply the change
        updated_staff[field] = new_value

    return updated_staff


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempt
    try:
        new_record = modify_staff_info(
            employee,
            {"salary": 80000, "department": "Research"},
            admin_status=False
        )
        print("Non‑admin update succeeded:", new_record)
    except ValueError as e:
        print(f"Non‑admin error: {e}")

    # Admin attempt
    new_record = modify_staff_info(
        employee,
        {"salary": 80000, "social_security_number": "987-65-4321"},
        admin_status=True
    )
    print("Admin update succeeded:", new_record)