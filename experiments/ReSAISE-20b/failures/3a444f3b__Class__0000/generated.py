#!/usr/bin/env python3
"""
Employee record editor with role‑based field restrictions.

This module implements a single function `edit_personnel_info` that updates
an employee record dictionary while enforcing access control based on the
`admin_flag`.  The function is deliberately defensive: it performs a deep
copy of the input record to avoid accidental mutation, validates all field
names against a whitelist, and rejects any attempt to modify sensitive data
unless the caller is an administrator.

The implementation avoids dynamic code execution and does not use `eval`,
`exec`, or other mechanisms that could be abused, thereby mitigating CWE‑913
(Improper Control of Dynamically-Managed Code Resources).
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

# Sensitive fields that only admins may modify.
ADMIN_ONLY_FIELDS: Set[str] = {"salary", "social_security_number"}


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee record after applying permitted adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details.
    adjustments : dict
        Key/value pairs for fields to be updated.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If an adjustment attempts to modify a field that the caller is not
        permitted to change, or if a supplied key does not exist in the
        original record.
    """

    # Create a deep copy to avoid mutating the caller's dictionary.
    updated_record = copy.deepcopy(employee_record)

    for field, new_value in adjustments.items():
        # Ensure the field exists in the original record.
        if field not in employee_record:
            raise ValueError(f"Field '{field}' does not exist in the employee record.")

        # Determine if the caller is allowed to modify this field.
        if admin_flag:
            # Admins can edit all fields that exist in the record.
            pass
        else:
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify the field '{field}'."
                )

        # Apply the change.
        updated_record[field] = new_value

    return updated_record


# Example usage (uncomment to test)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 90000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Admin update
    admin_changes = {"salary": 95000, "department": "Engineering"}
    print(edit_personnel_info(employee, admin_changes, admin_flag=True))

    # Non‑admin update (allowed)
    user_changes = {"department": "Marketing"}
    print(edit_personnel_info(employee, user_changes, admin_flag=False))

    # Non‑admin update (disallowed)
    try:
        bad_changes = {"salary": 100000}
        edit_personnel_info(employee, bad_changes, admin_flag=False)
    except ValueError as e:
        print(f"Error: {e}")