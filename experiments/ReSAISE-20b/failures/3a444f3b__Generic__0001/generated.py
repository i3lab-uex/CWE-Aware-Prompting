#!/usr/bin/env python3
"""
Utility to safely edit employee records.

The module defines a single public function `edit_personnel_info` that
updates an employee record dictionary according to the supplied changes,
respecting permission rules and preventing accidental modification of
sensitive fields such as `social_security_number`.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}

# All supported fields in an employee record.
ALL_FIELDS = {"name", "position", "salary", "department", "social_security_number"}


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee record after applying valid adjustments.

    Parameters
    ----------
    employee_record : dict
        Current state of the employee's details. Must contain all keys in
        ``ALL_FIELDS``.
    adjustments : dict
        Proposed changes. Keys are field names, values are the new data.
    admin_flag : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary with the applied changes.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field, or if an unknown
        field is supplied.
    TypeError
        If ``employee_record`` or ``adjustments`` are not dictionaries.

    Notes
    -----
    The function performs a shallow copy of the original record and only
    applies changes that are permitted. It does not attempt to validate data
    types beyond checking that the record and adjustments are dictionaries.
    """

    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")

    # Validate that the employee record contains all expected fields
    missing = ALL_FIELDS - set(employee_record.keys())
    if missing:
        raise ValueError(f"Employee record is missing fields: {missing}")

    # Prepare a new dictionary to avoid mutating the input
    updated_record = copy.deepcopy(employee_record)

    for field, new_value in adjustments.items():
        # Unknown field
        if field not in ALL_FIELDS:
            raise ValueError(f"Unknown field '{field}' in adjustments")

        # Non-admins cannot modify protected fields
        if not admin_flag and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non-admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_record[field] = new_value

    return updated_record


# Example usage (uncomment to test)
if __name__ == "__main__":
    emp = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 75000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    changes = {"salary": 80000, "department": "Product"}
    try:
        new_emp = edit_personnel_info(emp, changes, admin_flag=False)
        print(new_emp)
    except Exception as e:
        print(f"Error: {e}")