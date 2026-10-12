#!/usr/bin/env python3
"""
Employee record updater.

The module defines a single public function `update_employee_record` that safely updates
an employee dictionary according to the rules below:

* Regular users may only modify fields listed in `EDITABLE_FIELDS`.
* Admins can modify any field.
* Unknown update keys are ignored (no error is raised).
* The original employee dictionary is not mutated; a new dict instance is returned.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Global set of fields that can be updated by regular users.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


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
        Dictionary representing the current state of an employee.
    updates : dict
        Dictionary containing fields to update and their new values.
    is_admin : bool
        Flag indicating whether the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Notes
    -----
    * The function never mutates the input `employee` dictionary.
    * Only fields present in `updates` that are allowed for the caller
      (according to `EDITABLE_FIELDS`) will be applied.
    * Admins can modify any field; regular users are restricted.
    """
    # Defensive copy to avoid side effects
    updated = copy.deepcopy(employee)

    for key, value in updates.items():
        # If the caller is not an admin and the field is not editable, skip it
        if not is_admin and key not in EDITABLE_FIELDS:
            continue

        # Only update keys that already exist in the employee record
        if key in updated:
            updated[key] = value

    return updated