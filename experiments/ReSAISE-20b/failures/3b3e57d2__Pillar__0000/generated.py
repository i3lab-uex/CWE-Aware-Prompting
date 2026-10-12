#!/usr/bin/env python3
"""
Utility to modify employee records with fine‑grained access control.

The module defines:
    * EDITABLE_FIELDS – a set of keys that regular users are allowed to modify.
    * modify_staff_details() – applies changes to an employee record while
      enforcing the permissions defined by EDITABLE_FIELDS.

Security notes:
    * Only keys present in `employee_data` may be modified.
    * Regular users can only touch the fields listed in EDITABLE_FIELDS.
    * Superusers (admins) may modify any field.
    * The function operates on a shallow copy of the input to avoid
      accidental mutation of caller‑supplied data.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that non‑admin users may edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary after applying the supplied changes.

    Parameters
    ----------
    employee_data:
        The original employee record.
    changes:
        A mapping of fields to new values.
    is_superuser:
        If True, all changes are allowed.  If False, only fields in
        EDITABLE_FIELDS may be altered.

    Returns
    -------
    dict:
        A new dictionary containing the updated employee record.

    Raises
    ------
    ValueError
        If a regular user attempts to modify a non‑editable field.
    KeyError
        If a change references a key that does not exist in the employee record.

    Notes
    -----
    The function performs a shallow copy of ``employee_data``; nested mutable
    objects are not deep‑copied.  This is sufficient for the intended use case
    and avoids unnecessary memory usage.
    """
    # Defensive copy to avoid side effects on the caller's data
    updated = copy.copy(employee_data)

    for field, new_value in changes.items():
        if field not in employee_data:
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify field '{field}' for non‑admin users."
            )

        updated[field] = new_value

    return updated