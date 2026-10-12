# -*- coding: utf-8 -*-
"""
Utility module for staff record modification.

The function ``modify_staff_info`` updates an employee dictionary while enforcing
access control.  Non‑admin users may only modify the fields listed in
``EDITABLE_FIELDS``; all other changes raise an exception.
"""

from __future__ import annotations

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def _validate_changes(changes: dict) -> None:
    """
    Basic validation to ensure the changes dictionary contains only hashable keys.
    Raises a TypeError if any key is not a string.
    """
    for key in changes:
        if not isinstance(key, str):
            raise TypeError(f"Change key {key!r} is not a string")

def modify_staff_info(
    staff: dict,
    changes: dict,
    admin_status: bool
) -> dict:
    """
    Return a new staff dictionary with the requested changes applied.

    Parameters
    ----------
    staff : dict
        Current employee record.  Must contain at least the keys:
            * ``name``
            * ``position``
            * ``salary``
            * ``department``
            * ``social_security_number``

    changes : dict
        Mapping of fields to their new values.

    admin_status : bool
        ``True`` if the caller is an administrator and may modify any field.
        ``False`` restricts updates to those listed in :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a disallowed field.

    TypeError
        If the changes dictionary contains non‑string keys.
    """
    if not isinstance(staff, dict):
        raise TypeError("staff must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    _validate_changes(changes)

    # Start with a shallow copy to avoid mutating the original
    updated_staff = staff.copy()

    for field, new_value in changes.items():
        if not admin_status and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be modified by non‑admin users."
            )
        # Allow the update
        updated_staff[field] = new_value

    return updated_staff