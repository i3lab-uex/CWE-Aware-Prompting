#!/usr/bin/env python3
"""
Utility to safely modify employee data.

The function enforces that non‑admin users can only change a limited set of fields
defined in the global `EDITABLE_FIELDS` set. Admins may modify any field.

The implementation follows defensive programming practices:
- It performs type checks and raises informative exceptions.
- It creates a copy of the employee record to avoid accidental mutation
  of external references (CWE‑664: improper control of a resource).
"""

from __future__ import annotations

from typing import Dict, Any, Set


# Fields that regular users are allowed to edit
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}


def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Return a new dictionary representing the updated employee record.

    Parameters
    ----------
    worker : dict
        The original employee data. Must be a mapping of string keys to any values.
    alterations : dict
        Proposed changes keyed by field name. Keys not present in the worker are ignored.
    admin_privileges : bool
        If True, all fields may be modified. Otherwise only `EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If `worker` or `alterations` are not dictionaries.
    ValueError
        If a non‑admin user attempts to modify a protected field or if an alteration
        references a key not present in the original record.
    """
    # --- Basic type validation ---------------------------------------------
    if not isinstance(worker, dict):
        raise TypeError(f"worker must be a dict; got {type(worker).__name__}")
    if not isinstance(alterations, dict):
        raise TypeError(f"alterations must be a dict; got {type(alterations).__name__}")

    # --- Defensive copy to avoid side‑effects -------------------------------
    updated_worker: Dict[str, Any] = worker.copy()

    # --- Process each alteration --------------------------------------------
    for field, new_value in alterations.items():
        if field not in worker:
            raise ValueError(f"Attempted to modify unknown field '{field}'")

        # Enforce permissions
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'. "
                "Only {EDITABLE_FIELDS} are editable."
            )

        # Apply the change
        updated_worker[field] = new_value

    return updated_worker


# Example usage (uncomment to test)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Developer", "salary": 95000}

    # Regular user attempting to change salary (should raise ValueError)
    try:
        modify_employee_data(employee, changes, admin_privileges=False)
    except ValueError as e:
        print(f"Regular user error: {e}")

    # Admin updating salary
    updated = modify_employee_data(employee, changes, admin_privileges=True)
    print("Updated employee:", updated)