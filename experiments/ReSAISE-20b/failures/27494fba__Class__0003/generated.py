#!/usr/bin/env python3
"""
Employee profile adjustment module.

This module provides a single public function, `adjust_employee_profile`, which
applies user‑requested changes to an employee record while enforcing strict
permissions.  Only users with administrative rights may modify arbitrary fields;
regular users are limited to a predefined set of editable attributes.

The implementation deliberately avoids executing any dynamic code or
interpreting values that could lead to CWE‑913 (Improper Control of
Dynamically‑Managed Code Resources) vulnerabilities.  All inputs are treated as
plain data structures, and no string evaluation or code injection is performed.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration: fields that regular users may edit
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Salary changes are typically reserved for admins, but if desired,
    # uncomment the following line to allow non‑admin updates.
    # "salary",
}


def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Apply a set of proposed changes to an employee dictionary.

    Parameters
    ----------
    emp : dict
        Original employee record.  Must be a mapping of string keys to values.
    changes : dict
        Proposed modifications keyed by attribute name.  Values are assigned
        directly; no type coercion or validation beyond permissions.
    has_admin_rights : bool
        If True, the caller is an administrator and may modify any field.
        Otherwise only fields listed in :data:`EDITABLE_FIELDS` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.  The input
        ``emp`` is not mutated.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in ``EDITABLE_FIELDS``.
    TypeError
        If any of the arguments are not dictionaries or if ``changes`` is
        empty (no-op changes are disallowed to avoid accidental no‑ops).
    """
    # Basic type validation
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Prevent accidental no‑op
    if not changes:
        raise ValueError("changes dictionary is empty; nothing to update")

    # Create a shallow copy so the original dict remains untouched
    updated_emp = copy.deepcopy(emp)

    for field, new_value in changes.items():
        # Skip non‑string keys to avoid accidental injection
        if not isinstance(field, str):
            raise ValueError(f"Field name must be a string; got {field!r}")

        # Permission check
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify '{field}'. "
                "Only editable fields are: "
                f"{sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated_emp[field] = new_value

    return updated_emp


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin changing salary and SSN
    admin_changes = {"salary": 95000, "social_security_number": "987-65-4321"}
    updated = adjust_employee_profile(employee, admin_changes, has_admin_rights=True)
    print("Admin update:", updated)

    # Regular user attempting to change position
    user_changes = {"position": "Senior Developer"}
    updated_user = adjust_employee_profile(employee, user_changes, has_admin_rights=False)
    print("User update:", updated_user)

    # Regular user attempting to change salary (should raise)
    try:
        bad_change = {"salary": 100000}
        adjust_employee_profile(employee, bad_change, has_admin_rights=False)
    except ValueError as exc:
        print("Expected error:", exc)