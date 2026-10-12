#!/usr/bin/env python3
"""
Employee record update module.

This module defines a single function `update_employee_record` that safely updates
an employee record.  The update is only allowed for fields listed in the global
`EDITABLE_FIELDS` set unless the caller has admin privileges.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Define which fields can be modified by regular users.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}  # salary and SSN are protected

def update_employee_record(
    employee: dict,
    updates: dict,
    is_admin: bool = False
) -> dict:
    """
    Update an employee record with the provided changes.

    Parameters
    ----------
    employee : dict
        The original employee data.  Must contain at least the keys:
        `name`, `position`, `salary`, `department`,
        and `social_security_number`.
    updates : dict
        A mapping of fields to new values.
    is_admin : bool, optional
        If ``True`` the caller may modify any field.  Defaults to ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If `updates` is not a mapping.
    PermissionError
        If the user attempts to modify a protected field without admin rights.

    Notes
    -----
    The function performs shallow copying; nested objects are not deeply cloned.
    """
    if not isinstance(updates, dict):
        raise ValueError("`updates` must be a dictionary")

    # Copy the original record to avoid mutating input
    updated = employee.copy()

    for field, new_value in updates.items():
        if not is_admin and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Field '{field}' cannot be modified by a non-admin user"
            )
        updated[field] = new_value

    return updated