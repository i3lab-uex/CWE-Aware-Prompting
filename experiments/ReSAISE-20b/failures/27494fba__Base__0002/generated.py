# -*- coding: utf-8 -*-

"""
Employee profile updater.

The module defines a global set of fields that regular users may edit.
An admin user can modify any field.

CWE-915 mitigated by validating the keys in `changes` against
the allowed set before applying them to the employee dictionary.
"""

from __future__ import annotations

# Global set of fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

def adjust_employee_profile(
    emp: dict,
    changes: dict,
    has_admin_rights: bool
) -> dict:
    """
    Update an employee dictionary with the provided changes.

    Parameters
    ----------
    emp : dict
        The original employee record.  Keys are attribute names.
    changes : dict
        Proposed modifications.  Each key must be a valid field name.
    has_admin_rights : bool
        If True, all fields may be updated.  Otherwise only keys in
        ``EDITABLE_FIELDS`` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.
        The original `emp` is not modified.

    Raises
    ------
    ValueError
        If a key in `changes` is not allowed for the caller.
    TypeError
        If any of the arguments are not of expected type.

    Notes
    -----
    The function performs shallow copying; nested objects are shared.
    """
    # Basic type checks
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Determine allowed fields
    if has_admin_rights:
        allowed_fields = set(emp.keys()) | set(changes.keys())
    else:
        allowed_fields = EDITABLE_FIELDS

    # Validate all requested changes
    disallowed = [k for k in changes if k not in allowed_fields]
    if disallowed:
        raise ValueError(
            f"Unauthorized modification attempt for fields: {', '.join(disallowed)}"
        )

    # Create a copy to avoid mutating the original
    updated_emp = emp.copy()
    updated_emp.update(changes)
    return updated_emp