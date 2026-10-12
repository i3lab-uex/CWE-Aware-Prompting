# -*- coding: utf-8 -*-
"""
Employee detail modification utility.

The module defines a single public function `modify_staff_details` which
applies changes to an employee record while enforcing access control.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Fields that a non‑superuser is allowed to modify.
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
    Apply a set of changes to an employee record.

    Parameters
    ----------
    employee_data : dict
        The original employee dictionary.  Must contain at least the keys
        defined in ``EDITABLE_FIELDS`` and any sensitive fields.
    changes : dict
        Proposed modifications.  Keys must be a subset of the employee's
        existing keys.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.  The original
        ``employee_data`` is left untouched.

    Raises
    ------
    ValueError
        If a requested change targets a field that does not exist in the
        employee record or if a non‑superuser attempts to modify a field
        outside ``EDITABLE_FIELDS``.
    """
    # Defensive copy – the caller's dictionary must not be mutated.
    updated = copy.deepcopy(employee_data)

    # Validate that all keys in ``changes`` exist in the employee record.
    for key in changes:
        if key not in updated:
            raise ValueError(f"Field '{key}' does not exist in employee record")

    # Enforce field‑level permissions.
    for key, new_value in changes.items():
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient permissions to modify field '{key}'"
            )
        # Apply the change.
        updated[key] = new_value

    return updated