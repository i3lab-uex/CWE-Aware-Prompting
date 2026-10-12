#!/usr/bin/env python3
"""
Employee data modification utility.

This module provides a single function `modify_staff_details` that updates an
employee record while enforcing strict field‑level permissions.  It protects
against CWE-915 by ensuring that only explicitly allowed fields can be
modified when the caller is not a superuser.  Superusers may modify any field.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Fields that regular users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {"position", "department", "salary"}


def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new dictionary with the employee data updated according to
    *changes*, respecting field‑level permissions.

    Parameters
    ----------
    employee_data:
        The original employee record.  Keys represent attribute names.
    changes:
        Proposed modifications.  Keys must be a subset of the existing
        attributes in *employee_data*.
    is_superuser:
        If ``True`` the caller has full modification rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If *changes* contains a key that does not exist in *employee_data*.
    PermissionError
        If a non‑superuser attempts to modify a field not in `EDITABLE_FIELDS`.
    """
    # Validate that all requested changes refer to existing attributes
    for key in changes:
        if key not in employee_data:
            raise KeyError(f"Attempted to modify non‑existent field '{key}'")

    # Determine which fields are allowed to be changed
    if is_superuser:
        allowed_keys = set(changes.keys())
    else:
        allowed_keys = {k for k in changes if k in EDITABLE_FIELDS}

    # Build a shallow copy of the original data
    updated = copy.deepcopy(employee_data)

    # Apply allowed changes only
    for key in allowed_keys:
        updated[key] = changes[key]

    # If there were any prohibited fields, raise an error
    if not is_superuser:
        forbidden = set(changes) - allowed_keys
        if forbidden:
            raise PermissionError(
                f"User lacks permission to modify fields: {', '.join(sorted(forbidden))}"
            )

    return updated


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     emp = {"name": "Jane Doe", "position": "Developer", "salary": 70000,
#            "department": "Engineering", "social_security_number": "123-45-6789"}
#     changes = {"salary": 75000, "department": "Research", "name": "Jane D."}
#     print(modify_staff_details(emp, changes, is_superuser=False))