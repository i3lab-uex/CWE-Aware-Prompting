# -*- coding: utf-8 -*-

"""
Employee profile adjustment module.

This module provides a single public function `adjust_employee_profile` that
updates an employee dictionary according to the supplied changes, while
enforcing field‑level access control based on the user's privilege level.

Security considerations:
- Only keys present in `EDITABLE_FIELDS` can be modified by non‑admin users.
- Admins may modify any key, but still only those present in the original
  employee dictionary to avoid accidental creation of arbitrary keys.
- The function performs a shallow copy of the input dictionary to prevent
  accidental mutation of caller‑supplied data.
"""

from __future__ import annotations

from typing import Dict, Any

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}


def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Update an employee profile according to the supplied changes.

    Parameters
    ----------
    emp : dict
        Original employee data. Must be a mapping of string keys to values.
    changes : dict
        Proposed modifications. Keys are attribute names; values are the new
        values to assign.
    has_admin_rights : bool
        Flag indicating whether the caller is an administrator.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data. The original
        `emp` dictionary is not modified.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in `EDITABLE_FIELDS`.
    KeyError
        If an admin tries to modify a key that does not exist in the original
        employee dictionary.
    """
    # Validate input types early to avoid unexpected behaviour.
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # Create a shallow copy to avoid mutating the original employee data.
    updated_emp = emp.copy()

    for key, new_value in changes.items():
        # Normal users: enforce editable fields.
        if not has_admin_rights:
            if key not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify the field '{key}'."
                )
        else:
            # Admins: only allow updates to existing keys.
            if key not in emp:
                raise KeyError(
                    f"Admin attempted to modify non‑existent field '{key}'."
                )

        # Apply the change.
        updated_emp[key] = new_value

    return updated_emp