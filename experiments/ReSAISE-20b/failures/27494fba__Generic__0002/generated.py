#!/usr/bin/env python3
"""
Employee profile adjustment module.

This module provides a single function, `adjust_employee_profile`, which
updates an employee dictionary according to a set of proposed changes.
Non‑admin users are restricted to modifying only the fields listed in
`EDITABLE_FIELDS`. Admin users may modify any field.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration: fields that regular users are allowed to edit
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
}  # e.g. only these can be changed by non‑admins


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with the requested changes applied.

    Parameters
    ----------
    emp : dict
        The original employee record.
    changes : dict
        A mapping of attribute names to new values that should be applied.
    has_admin_rights : bool
        If ``True`` the caller is an administrator and may modify any field.
        If ``False`` only keys present in :data:`EDITABLE_FIELDS` may be updated.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field that is not in
        :data:`EDITABLE_FIELDS`.
    TypeError
        If any argument has an inappropriate type.
    """
    # Basic input validation
    if not isinstance(emp, dict):
        raise TypeError("emp must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Make a shallow copy to avoid mutating the caller's data
    updated_emp = copy.deepcopy(emp)

    # Apply changes, enforcing permissions for non‑admin users
    for key, value in changes.items():
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify field '{key}' without admin rights."
            )
        updated_emp[key] = value

    return updated_emp