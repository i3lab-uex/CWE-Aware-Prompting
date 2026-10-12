# -*- coding: utf-8 -*-
"""
Employee record modification utility.

This module defines the `alter_employee_details` function that applies
allowed changes to an employee's dictionary while enforcing access control.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global list of fields that non‑admin users may edit.
EDITABLE_FIELDS = [
    "name",
    "position",
    "department",
]


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Apply permitted changes to an employee record.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.
    
    Raises
    ------
    TypeError
        If ``emp_data`` or ``changes`` is not a mapping.
    ValueError
        * If a non‑admin attempts to modify a field outside ``EDITABLE_FIELDS``.
        * If any key in ``changes`` is not present in the original record.
    """
    if not isinstance(emp_data, dict):
        raise TypeError("emp_data must be a dictionary.")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary.")

    # Ensure all requested changes are legitimate
    for field in changes:
        if field not in emp_data:
            raise ValueError(f"Field '{field}' does not exist in employee record.")
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

    # Perform the update on a shallow copy to avoid mutating input
    updated = copy.deepcopy(emp_data)
    for field, new_value in changes.items():
        updated[field] = new_value

    return updated