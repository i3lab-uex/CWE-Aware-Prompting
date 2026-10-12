# -*- coding: utf-8 -*-

"""
Employee data modification module.

This module provides a single public function `modify_staff_details` that
updates an employee record while enforcing field‑level permissions.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set

# --------------------------------------------------------------------------- #
# Global configuration: which fields a regular user may edit
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def modify_staff_details(
    employee_data: Dict[str, Any],
    changes: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Update an employee record with the supplied changes.

    Parameters
    ----------
    employee_data : dict
        The current employee record.  Keys represent attributes such as
        ``name``, ``position``, ``salary`` etc.
    changes : dict
        Proposed modifications.  Each key must be a string that matches an
        attribute name in ``employee_data``.
    is_superuser : bool
        If ``True``, the caller has full editing rights and can modify any
        attribute.  If ``False`` only attributes listed in the global
        ``EDITABLE_FIELDS`` set may be altered.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``employee_data`` is left untouched.

    Raises
    ------
    KeyError
        If a key in ``changes`` does not exist in ``employee_data``.
    PermissionError
        If a non‑superuser attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    TypeError
        If either ``employee_data`` or ``changes`` is not a dictionary.

    Notes
    -----
    * The function performs a shallow copy of ``employee_data``; nested
      mutable structures are not deeply cloned.
    * No dynamic code execution is performed – all operations are
      dictionary lookups and assignments, preventing CWE‑913 style
      vulnerabilities.
    """
    # -------------------------------------------------------------------- #
    # Input validation
    # -------------------------------------------------------------------- #
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # -------------------------------------------------------------------- #
    # Prepare result (shallow copy)
    # -------------------------------------------------------------------- #
    updated = copy.copy(employee_data)

    # -------------------------------------------------------------------- #
    # Apply changes
    # -------------------------------------------------------------------- #
    for field, new_value in changes.items():
        if field not in employee_data:
            raise KeyError(f"Field '{field}' does not exist in the employee record")

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑superuser cannot modify field '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        updated[field] = new_value

    return updated