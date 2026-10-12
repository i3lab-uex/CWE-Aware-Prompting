#!/usr/bin/env python3
"""
Utility for safely editing employee records.

The module defines a single function `edit_personnel_info` that updates
an employee record dictionary according to the supplied adjustments.
Non‑admin users are only allowed to modify a predefined set of
editable fields.  All other modifications will raise an exception.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


def _validate_field(field: str, admin_flag: bool) -> None:
    """
    Ensure the field is present in the employee record and that
    a non‑admin user cannot modify restricted fields.

    Raises:
        KeyError: If the field is not present in a record.
        PermissionError: If a non‑admin tries to modify a restricted field.
    """
    if not admin_flag and field not in EDITABLE_FIELDS:
        raise PermissionError(
            f"Field '{field}' is not editable for non‑admin users."
        )


def edit_personnel_info(
    employee_record: Dict[str, Any],
    adjustments: Dict[str, Any],
    admin_flag: bool,
) -> Dict[str, Any]:
    """
    Return a new employee record dictionary with the requested adjustments.

    Parameters
    ----------
    employee_record : dict
        The current state of an employee's details.
    adjustments : dict
        Key‑value pairs indicating the fields to update and their new values.
    admin_flag : bool
        True if the updater is an administrator; otherwise False.

    Returns
    -------
    dict
        A new dictionary containing the updated employee information.

    Raises
    ------
    KeyError
        If an adjustment refers to a field not present in the original record.
    PermissionError
        If a non‑admin attempts to modify a restricted field.
    TypeError
        If the inputs are not dictionaries or if adjustments is None.
    """

    # Basic type checks
    if not isinstance(employee_record, dict):
        raise TypeError("employee_record must be a dictionary.")
    if not isinstance(adjustments, dict):
        raise TypeError("adjustments must be a dictionary.")
    if not isinstance(admin_flag, bool):
        raise TypeError("admin_flag must be a boolean.")

    # Work on a shallow copy to avoid mutating the input
    updated_record = copy.deepcopy(employee_record)

    for field, new_value in adjustments.items():
        # Ensure the field exists
        if field not in updated_record:
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        # Enforce edit permissions
        _validate_field(field, admin_flag)

        # Perform the update
        updated_record[field] = new_value

    return updated_record