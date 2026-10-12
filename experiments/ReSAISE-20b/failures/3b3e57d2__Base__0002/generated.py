# -*- coding: utf-8 -*-
"""
Employee data modification helper.

This module defines a single public function :func:`modify_staff_details` which
applies changes to an employee dictionary in a safe and controlled manner.
"""

from __future__ import annotations

from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}

# Fields that are considered sensitive and should never be modified by a
# non‑superuser.  They can still be modified if the caller is a superuser.
SENSITIVE_FIELDS: Set[str] = {"salary", "social_security_number"}


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Apply ``changes`` to ``employee_data`` while enforcing field‑level
    permissions.

    Parameters
    ----------
    employee_data : dict
        The original employee record.  It will **not** be modified in place;
        a new dictionary is returned.
    changes : dict
        Proposed modifications keyed by attribute name.
    is_superuser : bool
        ``True`` if the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a change attempts to modify a field that the caller is not allowed
        to touch, or if ``changes`` contains keys that do not exist in the
        employee record.

    Notes
    -----
    * The function does **not** perform type validation beyond checking that
      the field exists.  Consumers should validate data types if required.
    * The function is intentionally pure: it never mutates its inputs and
      returns a new object.
    """
    # Ensure we do not modify the original dictionary.
    updated = employee_data.copy()

    for field, new_value in changes.items():
        # Reject modifications to unknown fields.
        if field not in employee_data:
            raise ValueError(f"Attempted to modify unknown field '{field}'.")

        # Determine if the caller is allowed to change this field.
        can_modify = (
            is_superuser
            or (field in EDITABLE_FIELDS and field not in SENSITIVE_FIELDS)
        )

        if not can_modify:
            raise ValueError(
                f"User does not have permission to modify field '{field}'."
            )

        # Apply the change.
        updated[field] = new_value

    return updated