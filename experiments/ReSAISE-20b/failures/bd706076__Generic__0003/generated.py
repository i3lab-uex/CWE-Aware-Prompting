# -*- coding: utf-8 -*-

"""
Employee record updater.

The module defines a global set `EDITABLE_FIELDS` containing the names of
attributes that regular users may modify.  Admins can update any attribute.
"""

from __future__ import annotations

from typing import Dict, Any


# Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}


def _validate_update(employee: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """
    Validate that all keys in `updates` exist in the employee record.

    Raises:
        KeyError: If an update refers to a non‑existent field.
    """
    missing = set(updates) - employee.keys()
    if missing:
        raise KeyError(f"Unknown field(s) in update: {', '.join(sorted(missing))}")


def _check_permissions(updates: Dict[str, Any], is_admin: bool) -> None:
    """
    Ensure that a non‑admin user only attempts to modify editable fields.

    Raises:
        PermissionError: If a regular user tries to edit a protected field.
    """
    if is_admin:
        return
    non_editable = set(updates) - EDITABLE_FIELDS
    if non_editable:
        raise PermissionError(
            f"User does not have permission to edit field(s): "
            f"{', '.join(sorted(non_editable))}"
        )


def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with new values.

    Parameters
    ----------
    employee : dict
        The original employee dictionary.  Must contain keys such as
        ``name``, ``position``, ``salary`` and ``department``.
    updates : dict
        A mapping of field names to new values.  Keys must exist in the
        employee dictionary.
    is_admin : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If an update refers to a field that does not exist in the employee.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    """
    # Make a shallow copy so the original employee dict is not mutated.
    updated = employee.copy()

    # Validation
    _validate_update(employee, updates)
    _check_permissions(updates, is_admin)

    # Apply updates
    for field, value in updates.items():
        updated[field] = value

    return updated


# Example usage (commented out; remove comments to run):
#
# if __name__ == "__main__":
#     employee_data = {
#         "name": "Alice Smith",
#         "position": "Engineer",
#         "salary": 85000,
#         "department": "R&D",
#         "social_security_number": "123-45-6789"
#     }
#
#     # Regular user tries to change department
#     new_record = update_employee_record(
#         employee=employee_data,
#         updates={"department": "Marketing"},
#         is_admin=False
#     )
#     print(new_record)
#
#     # Admin changes salary (protected field)
#     admin_record = update_employee_record(
#         employee=employee_data,
#         updates={"salary": 90000},
#         is_admin=True
#     )
#     print(admin_record)