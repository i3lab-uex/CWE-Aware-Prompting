#!/usr/bin/env python3
"""
Utility to safely edit employee records.

The module exposes a single function `edit_personnel_info` that updates an
employee dictionary in accordance with the caller's permissions.  The function
prevents accidental or malicious changes to sensitive fields by only allowing
modification of a predefined set of editable keys unless the caller has admin
privileges.

Security notes:
- No dynamic code execution (`eval`, `exec`) is performed.
- The function works on a shallow copy of the input dictionary to avoid
  unintended side‑effects.
- Invalid keys or unauthorized updates raise clear, typed exceptions.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set

# Global set of fields that non‑admin users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool
) -> Dict[str, Any]:
    """
    Update an employee record with the provided adjustments.

    Parameters
    ----------
    employee_record : dict
        The original employee record.  Must contain all keys that may be updated.
    adjustments : dict
        Mapping of field names to new values.  Only keys present in the original
        record may be supplied.
    admin_flag : bool
        If ``True`` the caller is an administrator and may modify any field.
        Otherwise only fields listed in :data:`EDITABLE_FIELDS` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If an adjustment refers to a field that does not exist in the original
        record.
    PermissionError
        If a non‑admin user attempts to modify a field not in
        :data:`EDITABLE_FIELDS`.

    Notes
    -----
    The function performs a shallow copy of ``employee_record``; nested mutable
    objects are not deeply cloned.  This is sufficient for typical employee
    records that contain only primitive data types.
    """
    # Validate input types early to provide clear error messages
    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary")
    if not isinstance(admin_flag, bool):
        raise TypeError("admin_flag must be a boolean")

    # Work on a copy to avoid mutating the caller's dictionary
    updated_record = copy.deepcopy(employee_record)

    for field, new_value in adjustments.items():
        if field not in employee_record:
            raise KeyError(f"Field '{field}' does not exist in the employee record")

        if not admin_flag and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{field}'"
            )

        updated_record[field] = new_value

    return updated_record