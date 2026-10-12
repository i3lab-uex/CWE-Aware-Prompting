#!/usr/bin/env python3
"""
Employee record update module.

This module provides a single public function `update_employee_record` that safely
updates an employee dictionary.  The update operation respects a set of fields
that can be modified by regular users (`EDITABLE_FIELDS`).  Administrators are
allowed to modify any field except the employee's social security number,
which is treated as a protected attribute.

The implementation guards against CWE‑915 (Improperly Controlled Modification of
Dynamically-Determined Object Attributes) by validating all keys against a
whitelist before performing the update.
"""

from __future__ import annotations

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration: Fields that a non‑admin user is allowed to modify
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "salary",
    "department",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool = False,
) -> Dict[str, Any]:
    """
    Update an employee record with the provided changes.

    Parameters
    ----------
    employee : dict
        The original employee dictionary.  Must contain at least the keys that
        are expected to be updated.
    updates : dict
        A dictionary of fields to update and their new values.
    is_admin : bool, optional
        If ``True`` the caller has administrative privileges and may modify
        any field except ``social_security_number``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``employee`` dictionary is left untouched.

    Raises
    ------
    TypeError
        If either ``employee`` or ``updates`` is not a dictionary.
    KeyError
        If an update key does not exist in the employee record.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    ValueError
        If ``updates`` is empty.

    Notes
    -----
    The function deliberately avoids mutating the input dictionary to preserve
    immutability guarantees for callers that might rely on it.
    """

    if not isinstance(employee, dict):
        raise TypeError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise TypeError("updates must be a dictionary")

    if not updates:
        raise ValueError("No updates provided")

    # Create a shallow copy to avoid mutating the original
    updated_employee = employee.copy()

    for key, new_value in updates.items():
        if key not in employee:
            raise KeyError(f"Field '{key}' does not exist on the employee record")

        # Admins can modify any field except social_security_number
        if is_admin:
            if key == "social_security_number":
                raise PermissionError("Administrators cannot modify 'social_security_number'")
            updated_employee[key] = new_value
        else:
            if key not in EDITABLE_FIELDS:
                raise PermissionError(
                    f"Non‑admin users cannot modify '{key}'. "
                    f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
                )
            updated_employee[key] = new_value

    return updated_employee