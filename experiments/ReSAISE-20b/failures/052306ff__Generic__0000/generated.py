#!/usr/bin/env python3
"""
Employee record updater.

The module exposes a single public function :func:`alter_employee_details` that
applies changes to an employee dictionary.  Non‑superusers may only modify the
fields listed in :data:`EDITABLE_FIELDS`.  The function performs minimal type
checking and returns a new dictionary containing the updated data.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

# Fields that a non‑superuser is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def _validate_field_name(field: str) -> None:
    """Internal helper that checks if a field name is valid."""
    # In a real system this would check against the schema.  Here we simply
    # ensure it is a string and not empty.
    if not isinstance(field, str) or not field:
        raise ValueError(f"Invalid field name: {field!r}")


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee record after applying *changes*.

    Parameters
    ----------
    emp_data:
        Current state of the employee's details.
    changes:
        Mapping of field names to new values.
    is_superuser:
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary with the applied changes.

    Raises
    ------
    KeyError
        If *changes* contains a field that does not exist in ``emp_data``.
    PermissionError
        If a non‑superuser attempts to modify a protected field.
    ValueError
        If any key in *changes* is not a valid string.

    Notes
    -----
    The function makes a shallow copy of ``emp_data`` to avoid mutating the
    original dictionary.  If a change attempts to modify a field that is not
    present in the employee record, a :class:`KeyError` is raised to alert
    callers that they may be referencing an outdated or misspelled field.
    """
    # Defensive copy to avoid side‑effects
    updated = copy.deepcopy(emp_data)

    for field, new_value in changes.items():
        _validate_field_name(field)

        if field not in updated:
            raise KeyError(f"Field {field!r} does not exist in employee data")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin user cannot modify field {field!r}"
            )

        updated[field] = new_value

    return updated


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 95000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"salary": 100000, "department": "Research"}
    print("Original:", employee)

    # Superuser can change salary
    updated = alter_employee_details(employee, changes, is_superuser=True)
    print("Updated (superuser):", updated)

    # Non‑admin cannot change salary
    try:
        alter_employee_details(employee, changes, is_superuser=False)
    except PermissionError as exc:
        print("Permission error:", exc)