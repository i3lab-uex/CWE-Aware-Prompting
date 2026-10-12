#!/usr/bin/env python3
"""
Employee record updater.

This module defines a single function, `update_employee_record`, that safely updates
an employee dictionary.  Only fields listed in the global ``EDITABLE_FIELDS`` set can be
modified by non‑admin users.  Admins are allowed to modify any field.

The implementation guards against accidental modification of the original
dictionary by working on a shallow copy.  It also performs basic type checks
to prevent accidental injection of non‑serialisable objects.

CWE-913 (Improper Control of Dynamically-Managed Code Resources) is mitigated
by restricting write access to only known, permitted attributes.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Global set of fields that a regular user may edit.
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
}


def _validate_update(employee: Dict[str, Any], updates: Dict[str, Any]) -> None:
    """
    Perform basic validation of the update payload.

    Raises ValueError if any update attempts to modify a field that is not
    present in the employee dict or, for non‑admin users,
    attempts to modify a protected field.
    """
    for key in updates:
        if key not in employee:
            raise ValueError(f"Field '{key}' does not exist on the employee record.")
        # Ensure values are JSON‑serialisable (basic check)
        if isinstance(updates[key], (set, complex)):
            raise ValueError(f"Field '{key}' contains an unsupported type: {type(updates[key])}")


def update_employee_record(
    employee: Dict[str, Any], updates: Dict[str, Any], is_admin: bool
) -> Dict[str, Any]:
    """
    Update an employee record safely.

    Parameters
    ----------
    employee : dict
        The original employee dictionary.  This dictionary is **not** modified.
    updates : dict
        Mapping of field names to new values.
    is_admin : bool
        Flag indicating whether the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a requested field does not exist, or if a non‑admin attempts to modify
        a protected field.
    """
    # Create a shallow copy so the original remains untouched.
    updated = copy.deepcopy(employee)

    # Validate that all requested updates refer to existing fields
    _validate_update(employee, updates)

    for field, new_value in updates.items():
        if not is_admin and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"User does not have permission to modify the field '{field}'."
            )
        updated[field] = new_value

    return updated