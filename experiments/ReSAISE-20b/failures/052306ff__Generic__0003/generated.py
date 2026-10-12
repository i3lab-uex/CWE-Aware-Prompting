# -*- coding: utf-8 -*-
"""
Employee data modification module.

Provides a single public function:
    alter_employee_details(emp_data, changes, is_superuser)

The module defines a global list `EDITABLE_FIELDS` that specifies which
employee attributes may be edited by non‑superusers.  Superusers (admins)
are allowed to modify any field present in the employee dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# --------------------------------------------------------------------------- #
# Public constants
# --------------------------------------------------------------------------- #

#: Fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS: Iterable[str] = (
    "name",
    "position",
    "department",
)

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_changes(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> None:
    """
    Validate that all requested changes are permitted.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to change a field not in `EDITABLE_FIELDS`,
        or if a requested key does not exist in the employee data.
    """
    for field in changes:
        if field not in emp_data:
            raise ValueError(f"Field '{field}' does not exist in employee data.")
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot edit the field '{field}'."
            )

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Apply a set of changes to an employee record.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee's details.
    changes : dict
        Dictionary containing key-value pairs for fields to update.
    is_superuser : bool
        Flag indicating whether the updater has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        `emp_data` is left unmodified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a restricted field, or if the
        requested field does not exist in `emp_data`.
    """
    # Make a shallow copy to avoid mutating the caller's dictionary
    updated = copy.deepcopy(emp_data)

    # Validate changes before applying them
    _validate_changes(updated, changes, is_superuser)

    # Apply changes
    for key, value in changes.items():
        updated[key] = value

    return updated