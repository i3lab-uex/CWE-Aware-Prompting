# -*- coding: utf-8 -*-
"""
Utility module for updating employee records with role‑based access control.
"""

from typing import Dict, Any

# Fields that non‑admin users are allowed to modify
EDITABLE_FIELDS = {"name", "position", "department"}

class FieldModificationError(RuntimeError):
    """Raised when a user attempts to modify an unauthorized field."""
    pass


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the provided changes.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Desired updates, mapping field names to new values.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    FieldModificationError
        If a non‑admin attempts to modify a protected field.
    KeyError
        If any key in ``changes`` does not exist in the original record.

    Notes
    -----
    The function performs a shallow copy of ``emp_data`` before applying changes,
    ensuring the original dictionary is left untouched.
    """
    # Validate that all requested fields exist in the current record
    for key in changes:
        if key not in emp_data:
            raise KeyError(f"Field '{key}' does not exist in employee record.")

    # Enforce field‑level permissions
    if not is_superuser:
        unauthorized = set(changes) - EDITABLE_FIELDS
        if unauthorized:
            raise FieldModificationError(
                f"Non‑admin users cannot modify fields: {', '.join(sorted(unauthorized))}"
            )

    # Create a copy to avoid mutating the input dictionary
    updated_record = emp_data.copy()

    # Apply changes
    for key, value in changes.items():
        updated_record[key] = value

    return updated_record