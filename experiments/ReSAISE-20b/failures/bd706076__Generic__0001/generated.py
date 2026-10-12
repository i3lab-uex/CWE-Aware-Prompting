# -*- coding: utf-8 -*-
"""
Utility to update an employee record with validation and access control.
"""

from typing import Dict, Any

# Fields that regular users are allowed to edit
EDITABLE_FIELDS = {"name", "position", "department"}


def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the given changes.

    Parameters
    ----------
    employee : dict
        The original employee data.  Expected keys include:
        ``name``, ``position``, ``salary``, ``department``,
        and ``social_security_number``.
    updates : dict
        Mapping of field names to new values.  Only fields present in
        `EDITABLE_FIELDS` will be applied for regular users.
    is_admin : bool
        If ``True`` the caller has full update rights; otherwise only
        editable fields may be modified.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.
        The original `employee` object is not modified.

    Raises
    ------
    ValueError
        If a requested field to update is not present in the employee
        record or if an admin attempts to modify a non‑existent field.
    """

    # Create a copy so the original dict is not mutated
    updated = employee.copy()

    for field, value in updates.items():
        # Skip unknown fields – they are ignored silently
        if field not in employee:
            raise ValueError(f"Field '{field}' does not exist on the employee record.")

        # Regular users can only modify editable fields
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' is not editable by regular users."
            )

        # Perform the update
        updated[field] = value

    return updated