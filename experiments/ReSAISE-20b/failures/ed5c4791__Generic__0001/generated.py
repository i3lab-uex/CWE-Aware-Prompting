#!/usr/bin/env python3
"""
Utility for safely updating employee records.

The module defines a global set `EDITABLE_FIELDS` that lists the
attributes an ordinary user may modify.  Any attempt by a non‑admin to
change a field outside this set will raise a `PermissionError`.

The main function `modify_employee_data` accepts the current employee
dictionary, a dictionary of proposed changes, and a flag indicating
whether the caller has administrative privileges.  It returns a new
dictionary with the updates applied, leaving the original dictionary
unchanged.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Editable fields for regular users.  Admins can modify everything.
EDITABLE_FIELDS = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
def _validate_alterations(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> None:
    """
    Validate that each alteration is permissible.

    Raises:
        PermissionError: if a non‑admin attempts to modify a protected field.
        KeyError: if an alteration refers to a non‑existent attribute.
    """
    for field in alterations:
        if field not in worker:
            raise KeyError(f"Unknown employee attribute: {field!r}")

        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Insufficient privileges to modify '{field}'. "
                "Only admins may alter this field."
            )

def _apply_alterations(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return a new dictionary with the alterations applied.
    """
    updated = worker.copy()
    updated.update(alterations)
    return updated

def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Safely modify an employee record.

    Parameters
    ----------
    worker : dict
        Current employee data.  Expected keys include at least:
        ``name``, ``position``, ``salary``, ``department``,
        ``social_security_number``.
    alterations : dict
        Proposed changes.  Keys must match existing employee attributes.
    admin_privileges : bool
        If ``True``, all fields may be modified.  Otherwise only the
        attributes listed in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If an alteration refers to a non‑existent attribute.
    PermissionError
        If a regular user attempts to modify a protected field.
    """
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(admin_privileges, bool):
        raise TypeError("admin_privileges must be a boolean")

    _validate_alterations(worker, alterations, admin_privileges)
    return _apply_alterations(worker, alterations)

# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage
    employee = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 75000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Regular user attempting to change department (allowed)
    try:
        updated = modify_employee_data(
            employee,
            {"department": "Product"},
            admin_privileges=False
        )
        print("Updated employee:", updated)
    except Exception as exc:
        print(f"Error: {exc}")

    # Regular user attempting to change salary (disallowed)
    try:
        modify_employee_data(
            employee,
            {"salary": 80000},
            admin_privileges=False
        )
    except Exception as exc:
        print(f"Error: {exc}")

    # Admin changing salary
    updated_admin = modify_employee_data(
        employee,
        {"salary": 80000},
        admin_privileges=True
    )
    print("Admin updated employee:", updated_admin)