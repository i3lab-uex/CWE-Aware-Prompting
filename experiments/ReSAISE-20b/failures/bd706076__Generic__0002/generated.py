# -*- coding: utf-8 -*-

"""
Employee record update module.

The module exposes a single function `update_employee_record` which applies
updates to an employee dictionary.  Regular users may only modify fields
listed in the global `EDITABLE_FIELDS` set; administrators bypass this
restriction.

Security considerations:
- Only existing fields on the employee record are accepted.
- Attempts to modify non‑editable fields by a non‑admin raise
  `PermissionError`.
- The function returns a new dictionary, leaving the original unchanged.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Fields that regular users are allowed to edit.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}


def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested updates applied.

    Parameters
    ----------
    employee : dict
        The original employee record.  Must contain keys for all expected
        attributes.
    updates : dict
        Mapping of field names to new values.
    is_admin : bool
        If True, the caller has full editing privileges; otherwise only
        fields in `EDITABLE_FIELDS` may be modified.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If an update refers to a field that does not exist in the employee.
    PermissionError
        If a non‑admin attempts to modify a field outside `EDITABLE_FIELDS`.
    """
    # Validate that all update keys exist in the employee record.
    missing_keys = [k for k in updates if k not in employee]
    if missing_keys:
        raise KeyError(
            f"Attempted to update non‑existent fields: {', '.join(missing_keys)}"
        )

    # Check permissions for each field.
    if not is_admin:
        forbidden = [k for k in updates if k not in EDITABLE_FIELDS]
        if forbidden:
            raise PermissionError(
                f"Non‑admin users cannot modify fields: {', '.join(forbidden)}"
            )

    # Create a shallow copy to avoid mutating the original.
    updated_employee = copy.deepcopy(employee)

    # Apply updates.
    for field, new_value in updates.items():
        updated_employee[field] = new_value

    return updated_employee