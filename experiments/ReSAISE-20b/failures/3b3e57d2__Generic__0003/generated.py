#!/usr/bin/env python3
"""
Utility for safely modifying employee records.

The global `EDITABLE_FIELDS` defines which attributes a regular user
is allowed to modify.  Superusers (administrators) may change any field.
"""

from __future__ import annotations

import copy
from typing import Any, Dict


# Fields that a non‑superuser may edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    employee_data : dict
        Current state of an employee record.
    changes : dict
        Proposed modifications keyed by attribute name.
    is_superuser : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    KeyError
        If a requested change refers to an unknown field.
    PermissionError
        If a non‑superuser attempts to modify a protected field.
    """
    # Create a shallow copy; the values themselves are not modified in place
    updated = copy.deepcopy(employee_data)

    for field, new_value in changes.items():
        if field not in employee_data:
            raise KeyError(f"Field '{field}' does not exist on the employee record.")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑superusers may only edit the following fields: {sorted(EDITABLE_FIELDS)}."
            )

        updated[field] = new_value

    return updated