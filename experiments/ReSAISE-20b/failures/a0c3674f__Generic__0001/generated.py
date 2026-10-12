#!/usr/bin/env python3
"""
Utility module for updating employee records.

The main function, `modify_staff_info`, enforces that non‑admin users
can only modify a predefined set of fields.  Admin users are allowed to
modify any field present in the employee dictionary.

The function returns a **new** dictionary containing the updated
information and leaves the original input untouched.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Dict, Any

# -------------------------------------------------------------
# Global configuration – fields that can be edited by regular users
# -------------------------------------------------------------
EDITABLE_FIELDS = {"name", "position", "department"}

# -------------------------------------------------------------
# Public API
# -------------------------------------------------------------
def modify_staff_info(
    staff: Dict[str, Any],
    changes: Dict[str, Any],
    admin_status: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the supplied changes applied.

    Parameters
    ----------
    staff : dict
        Current state of an employee record.
    changes : dict
        Key/value pairs specifying the fields to update.
    admin_status : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If a requested field does not exist in the employee record.
    PermissionError
        If a non‑admin attempts to modify a field not in `EDITABLE_FIELDS`.
    TypeError
        If any of the arguments are not of the expected type.
    """
    # ---- Type checking ---------------------------------------
    if not isinstance(staff, dict):
        raise TypeError(f"staff must be a dict; got {type(staff).__name__}")
    if not isinstance(changes, dict):
        raise TypeError(f"changes must be a dict; got {type(changes).__name__}")
    if not isinstance(admin_status, bool):
        raise TypeError(f"admin_status must be a bool; got {type(admin_status).__name__}")

    # ---- Validate requested changes --------------------------
    for field in changes:
        if field not in staff:
            raise KeyError(f"Field '{field}' does not exist in the employee record")

        if not admin_status and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'"
            )

    # ---- Apply changes ---------------------------------------
    updated_staff = deepcopy(staff)
    for field, value in changes.items():
        updated_staff[field] = value

    return updated_staff


# -------------------------------------------------------------
# Example usage (removed from production code)
# -------------------------------------------------------------
if __name__ == "__main__":
    example_staff = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Admin modifies salary and department
    new_staff = modify_staff_info(
        staff=example_staff,
        changes={"salary": 95000, "department": "Research"},
        admin_status=True,
    )
    print("Updated staff:", new_staff)

    # Non‑admin attempts to modify salary (should raise PermissionError)
    try:
        modify_staff_info(
            staff=example_staff,
            changes={"salary": 100000},
            admin_status=False,
        )
    except PermissionError as exc:
        print("Permission error:", exc)