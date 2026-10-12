#!/usr/bin/env python3
"""
Employee record update module.

The function `alter_employee_details` updates an employee's data dictionary.
Non‑admin users may only modify fields listed in the global `EDITABLE_FIELDS`.
Superusers (admins) can change any field.  The function returns a **new**
dictionary and never mutates the input, preventing accidental resource
leaks or state corruption (CWE‑664).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def alter_employee_details(
    emp_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with validated changes applied.

    Parameters
    ----------
    emp_data : dict
        Current state of the employee record.
    changes : dict
        Desired updates as key/value pairs.
    is_superuser : bool
        If True, all fields may be updated.  Otherwise only
        `EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        Updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field, or if the
        requested change refers to a key that does not exist in `emp_data`.
    """
    # Defensive copy – avoid mutating the original dictionary.
    updated = copy.deepcopy(emp_data)

    for key, new_value in changes.items():
        # Ensure the field exists on the record.
        if key not in emp_data:
            raise ValueError(f"Field '{key}' does not exist in the employee record.")

        # Non‑admin users can only touch editable fields.
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

        # Apply the change.
        updated[key] = new_value

    return updated