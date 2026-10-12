# -*- coding: utf-8 -*-
"""
Utility module for employee profile adjustments.

The global `EDITABLE_FIELDS` defines which attributes a non‑admin user is allowed
to modify.  The function `adjust_employee_profile` applies the requested changes,
respecting these permissions and returning a new employee dictionary.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Editable fields for non‑admin users.  Admins may modify any field.
EDITABLE_FIELDS: frozenset[str] = frozenset(
    {
        "name",
        "position",
        "department",
    }
)


# --------------------------------------------------------------------------- #
class PermissionError(Exception):
    """Raised when a user attempts to modify a protected field."""


def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary after applying the requested changes.

    Parameters
    ----------
    emp : dict
        Original employee record.  The function does **not** modify this dictionary.
    changes : dict
        Proposed modifications keyed by attribute name.
    has_admin_rights : bool
        True if the caller is an administrator; otherwise only fields listed in
        `EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    PermissionError
        If a non‑admin attempts to modify a protected field.
    KeyError
        If `changes` contains keys that do not exist in the original employee record.
    """

    # Create a shallow copy to avoid mutating the input
    updated_emp = copy.deepcopy(emp)

    for field, new_value in changes.items():
        # Ensure the field exists on the original employee record
        if field not in emp:
            raise KeyError(f"Field '{field}' does not exist on the employee record.")

        # Non‑admin users may only modify a limited set of fields
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the change
        updated_emp[field] = new_value

    return updated_emp


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Simple demonstration of the function in action
    employee = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change the salary (should fail)
    try:
        adjust_employee_profile(
            emp=employee,
            changes={"salary": 80000},
            has_admin_rights=False,
        )
    except PermissionError as exc:
        print(f"Permission denied: {exc}")

    # Admin updating the salary (should succeed)
    updated = adjust_employee_profile(
        emp=employee,
        changes={"salary": 80000, "department": "Product"},
        has_admin_rights=True,
    )
    print("Updated employee:", updated)