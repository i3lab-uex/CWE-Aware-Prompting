#!/usr/bin/env python3
"""
Employee profile update utility.

This module defines a single function `adjust_employee_profile` that
modifies an employee dictionary while enforcing field‑level access control.
Non‑admin users may only change fields listed in the global `EDITABLE_FIELDS`
set. The function is safe against accidental modification of the original
employee dictionary and raises a clear exception if an unauthorized change
is attempted.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Configuration: fields that regular users are allowed to modify
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def adjust_employee_profile(
    emp: Dict[str, Any],
    changes: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary reflecting the requested changes.

    Parameters
    ----------
    emp : dict
        The original employee record. Keys may include, but are not limited to:
        ``name``, ``position``, ``salary``, ``department``,
        ``social_security_number``.
    changes : dict
        Proposed updates. Keys are attribute names; values are the new values.
    has_admin_rights : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the merged employee record.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field that is not in
        :data:`EDITABLE_FIELDS`.
    """
    # Work on a shallow copy to avoid mutating the caller's data
    updated_emp = copy.deepcopy(emp)

    for key, new_value in changes.items():
        # Skip unknown keys: they will simply be ignored
        if key not in emp:
            continue

        # Enforce field‑level access control for non‑admins
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field '{key}'. "
                "Only the following fields are editable: "
                f"{sorted(EDITABLE_FIELDS)}"
            )

        # Apply the change
        updated_emp[key] = new_value

    return updated_emp