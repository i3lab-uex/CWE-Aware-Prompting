# -*- coding: utf-8 -*-
"""
Utility module for staff data modification.

The core function `modify_staff_details` ensures that only authorized
attributes can be changed by non‑superusers.  It performs a shallow copy
of the original employee data to avoid accidental side effects.
"""

from __future__ import annotations

# Global set of fields that a regular user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

def modify_staff_details(
    employee_data: dict,
    changes: dict,
    is_superuser: bool
) -> dict:
    """
    Apply a set of proposed changes to an employee record.

    Parameters
    ----------
    employee_data : dict
        Current state of the employee.  Keys are attribute names.
    changes : dict
        Proposed modifications.  Each key must exist in `employee_data`.
    is_superuser : bool
        ``True`` if the caller has admin privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        * If `changes` contains keys not present in `employee_data`.
        * If a non‑superuser attempts to modify a protected field.
    TypeError
        If either `employee_data` or `changes` is not a mapping type.
    """
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the caller's data.
    updated = employee_data.copy()

    for key, new_value in changes.items():
        if key not in employee_data:
            raise ValueError(f"Unknown field '{key}' cannot be modified.")

        # Enforce edit permissions for regular users.
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{key}' is protected and cannot be modified by non‑superusers."
            )

        updated[key] = new_value

    return updated