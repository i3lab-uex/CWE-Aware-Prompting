#!/usr/bin/env python3
"""
Employee record updater.

This module defines a single function `update_employee_record` which updates an employee
dictionary in a controlled and secure manner.  It enforces that only fields listed in
`EDITABLE_FIELDS` may be modified by regular users.  Admins are exempt from this
restriction.

The function performs defensive copying to avoid mutating the original input and
validates its arguments for type safety.  It raises `ValueError` when an update
attempts to modify a protected field without sufficient privileges.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS: set[str] = {
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
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Update an employee record safely.

    Parameters
    ----------
    employee : dict
        The original employee dictionary.  Must contain keys such as
        'name', 'position', 'salary', 'department',
        and optionally 'social_security_number'.
    updates : dict
        A mapping of field names to new values.
    is_admin : bool
        If ``True``, the caller has administrative privileges and may update any field.
        If ``False`` only fields in :data:`EDITABLE_FIELDS` can be changed.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.  The original
        ``employee`` dictionary is left untouched.

    Raises
    ------
    ValueError
        If an attempt is made to update a non‑editable field without admin
        privileges, or if the input arguments are not dictionaries.

    Notes
    -----
    * The function performs a shallow copy of ``employee``.  Nested mutable objects
      (e.g., lists or dicts) are copied by reference; if deep copying is required,
      replace ``copy.copy`` with ``copy.deepcopy``.
    * This implementation follows the principle of least privilege and
      mitigates CWE-664 by ensuring that updates are only applied to valid fields.
    """
    # Argument validation
    if not isinstance(employee, dict):
        raise ValueError("employee must be a dictionary")
    if not isinstance(updates, dict):
        raise ValueError("updates must be a dictionary")
    if not isinstance(is_admin, bool):
        raise ValueError("is_admin must be a boolean")

    # Defensive copy to avoid mutating the caller's data
    updated = copy.copy(employee)

    for field, new_value in updates.items():
        # Admins can modify any field
        if is_admin or field in EDITABLE_FIELDS:
            updated[field] = new_value
        else:
            # Protect sensitive fields from unauthorized modification
            raise ValueError(
                f"Insufficient privileges to modify field '{field}'. "
                "Only admins can change it."
            )

    return updated