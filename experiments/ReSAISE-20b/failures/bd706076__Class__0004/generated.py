#!/usr/bin/env python3
"""
Employee record update module.

This module provides a single function, `update_employee_record`, which
updates an employee dictionary in a safe and controlled manner.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {"name", "position", "salary", "department"}


def update_employee_record(
    employee: Dict[str, Any],
    updates: Dict[str, Any],
    is_admin: bool,
) -> Dict[str, Any]:
    """
    Return a new employee dictionary with requested updates applied.

    Parameters
    ----------
    employee : dict
        The original employee record.  It must contain at least the keys:
        ``name``, ``position``, ``salary``, ``department`` and
        ``social_security_number``.  The function does **not** modify the
        original dictionary.
    updates : dict
        Mapping of field names to new values.  Only keys that exist in the
        original record may be updated.
    is_admin : bool
        ``True`` if the caller has administrative privileges and may modify
        any field, including those that are normally read‑only.

    Returns
    -------
    dict
        A new dictionary containing the updated employee record.

    Raises
    ------
    KeyError
        If an update refers to a field that does not exist in the original
        record.
    PermissionError
        If a non‑admin attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    ValueError
        If any of the values is not a plain data type (e.g. functions,
        classes).  This guards against accidental injection of executable
        code into the record.

    Notes
    -----
    The function performs a shallow copy of the original dictionary to avoid
    side‑effects.  All new values are validated to be JSON‑serialisable
    primitives (int, float, str, bool, None).  This mitigates CWE‑913
    by preventing the dynamic addition or modification of executable code.
    """
    # Defensive copy to avoid mutating the caller's data
    new_employee = copy.deepcopy(employee)

    for field, value in updates.items():
        if field not in employee:
            raise KeyError(f"Field '{field}' does not exist in the employee record.")

        # Permission check
        if not is_admin and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"User does not have permission to modify '{field}'."
            )

        # Basic type validation – only allow JSON‑serialisable primitives
        if not isinstance(value, (int, float, str, bool)) and value is not None:
            raise ValueError(
                f"Invalid type for field '{field}': {type(value).__name__}. "
                "Only int, float, str, bool, or None are allowed."
            )

        new_employee[field] = value

    return new_employee