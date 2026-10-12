# -*- coding: utf-8 -*-
"""
Safe employee record updater.

The function ensures that only whitelisted fields can be updated by
non‑admin users, protecting against CWE-915: Improperly Controlled Modification of Dynamically‑Determined Object Attributes.
"""

from __future__ import annotations

# Public API
__all__ = ["update_employee_record", "EDITABLE_FIELDS"]

# Whitelisted fields that a regular user may modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}

def update_employee_record(
    employee: dict,
    updates: dict,
    is_admin: bool = False
) -> dict:
    """
    Return a new employee dictionary with the requested updates applied.

    Parameters
    ----------
    employee : dict
        Existing employee record. Must contain at least the keys listed in
        ``EDITABLE_FIELDS`` and may contain other immutable fields.
    updates : dict
        Mapping of field names to new values.
    is_admin : bool, optional
        If ``True`` the caller bypasses the whitelist and may update any field.
        Defaults to ``False``.

    Returns
    -------
    dict
        A shallow copy of ``employee`` with the updates applied.

    Raises
    ------
    ValueError
        If a requested field is not present in the employee record or, for
        non‑admin users, if it is not in ``EDITABLE_FIELDS``.
    TypeError
        If ``employee`` or ``updates`` is not a mapping type.
    """
    # Validate input types
    if not isinstance(employee, dict):
        raise TypeError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    # Ensure all requested fields exist in the original record
    for field in updates:
        if field not in employee:
            raise ValueError(f"Field '{field}' does not exist on the employee record")

        # Enforce whitelist for non‑admin users
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(f"Field '{field}' cannot be updated by non‑admin users")

    # Create a shallow copy to avoid mutating the caller's dictionary
    updated = employee.copy()

    # Apply updates safely
    for field, value in updates.items():
        updated[field] = value

    return updated