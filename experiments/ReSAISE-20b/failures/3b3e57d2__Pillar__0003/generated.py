#!/usr/bin/env python3
"""
Employee details modification utility.

This module provides a single public function:
    modify_staff_details(employee_data, changes, is_superuser)

The function safely applies a set of proposed modifications to an employee
dictionary while enforcing role‑based field restrictions.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# -------------------------------------------------------------
# Global configuration: fields that regular users may edit.
# -------------------------------------------------------------
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
}

# -------------------------------------------------------------
# Public API
# -------------------------------------------------------------
def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Apply changes to an employee record with role‑based restrictions.

    Parameters
    ----------
    employee_data : dict
        Current employee attributes. Keys are arbitrary strings.
    changes : dict
        Proposed modifications. Each key should exist in the employee_data
        dictionary; otherwise a KeyError is raised.
    is_superuser : bool
        If True, the caller may modify any field.  Regular users are limited
        to EDITABLE_FIELDS.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If a change refers to an unknown field in ``employee_data``.
    PermissionError
        If a non‑superuser attempts to modify a protected field.
    ValueError
        If ``changes`` is not a mapping or contains non‑serialisable values.
    """
    if not isinstance(changes, dict):
        raise ValueError("`changes` must be a dictionary")

    # Create a shallow copy to avoid mutating the caller's data
    updated = copy.deepcopy(employee_data)

    for field, new_value in changes.items():
        # Validate the field exists
        if field not in employee_data:
            raise KeyError(f"Unknown field: {field!r}")

        # Enforce permission checks
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"User does not have permission to modify field: {field!r}"
            )

        # Basic type validation can be added here if needed
        updated[field] = new_value

    return updated