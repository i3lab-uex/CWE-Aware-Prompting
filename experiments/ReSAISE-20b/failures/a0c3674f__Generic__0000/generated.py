# -*- coding: utf-8 -*-

"""
Utility module for modifying employee records.

The `modify_staff_info` function ensures that only authorized fields are updated
by non‑admin users, preventing accidental or malicious changes to sensitive data.
"""

from __future__ import annotations

# Fields that non‑admin users are allowed to modify
EDITABLE_FIELDS = {"name", "position", "department"}

def _validate_fields(staff: dict, changes: dict, admin_status: bool) -> None:
    """
    Validate that all requested changes are permissible.

    Raises:
        KeyError: If a change refers to a non‑existent field.
        PermissionError: If a non‑admin attempts to modify an uneditable field.
    """
    for key in changes:
        if key not in staff:
            raise KeyError(f"Field '{key}' does not exist in the employee record.")
        if not admin_status and key not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

def modify_staff_info(
    staff: dict,
    changes: dict,
    admin_status: bool
) -> dict:
    """
    Return an updated employee record with validated changes.

    Parameters
    ----------
    staff : dict
        Current state of the employee's details.
    changes : dict
        Key/value pairs representing desired updates.
    admin_status : bool
        Flag indicating whether the updater is an administrator.

    Returns
    -------
    dict
        A new dictionary reflecting the applied changes.

    Raises
    ------
    KeyError
        If a requested field does not exist in the original record.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    """
    # Work on a shallow copy to avoid mutating the original dictionary
    updated_staff = staff.copy()

    # Validate before applying any changes
    _validate_fields(updated_staff, changes, admin_status)

    # Apply the allowed modifications
    for key, value in changes.items():
        updated_staff[key] = value

    return updated_staff