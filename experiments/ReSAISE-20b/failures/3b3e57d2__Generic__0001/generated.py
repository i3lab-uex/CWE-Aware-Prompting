#!/usr/bin/env python3
"""
Utility to modify employee data with field‑level permissions.
"""

from copy import deepcopy
from typing import Dict, Any

# Global set of fields that regular users are allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new dictionary with the requested changes applied to an employee record.

    Parameters
    ----------
    employee_data : dict
        Current employee data.
    changes : dict
        Proposed modifications. Keys must exist in ``employee_data``.
    is_superuser : bool
        If True, all fields may be updated. Otherwise only keys in
        ``EDITABLE_FIELDS`` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If ``changes`` contains keys that do not exist in the employee data,
        or if a non‑superuser attempts to modify a protected field.
    """
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Work on a copy to avoid mutating the original
    updated = deepcopy(employee_data)

    for field, new_value in changes.items():
        if field not in employee_data:
            raise ValueError(f"Field '{field}' does not exist in employee data")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: non‑superuser cannot modify '{field}'"
            )

        updated[field] = new_value

    return updated