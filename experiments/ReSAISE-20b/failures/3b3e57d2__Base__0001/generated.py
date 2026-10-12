#!/usr/bin/env python3
"""
Secure employee detail modification module.

This module defines a single function `modify_staff_details` that updates an
employee record while enforcing strict access control.  Regular users may only
change a pre‑defined set of fields (`EDITABLE_FIELDS`).  Superusers (admin
accounts) are allowed to modify any field present in the employee record.

The implementation guards against CWE‑915 (Improperly Controlled
Modification of Dynamically-Determined Object Attributes) by validating the
`changes` dictionary and rejecting any attempt to alter protected fields.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
#  Global configuration: fields that non‑admin users are allowed to edit
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "department"}

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
        The original employee record.  Keys represent attributes such as
        'name', 'position', 'salary', etc.
    changes : dict
        Proposed modifications.  Each key should correspond to a field in
        `employee_data`.  The values are the new data for those fields.
    is_superuser : bool
        ``True`` if the caller has administrative privileges; otherwise
        ``False``.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If `employee_data` or `changes` is not a dictionary.
    ValueError
        If a non‑admin user attempts to modify a protected field, or if
        `changes` contains keys that do not exist in the employee record.

    Notes
    -----
    * The function performs a shallow copy of `employee_data` before applying
      changes to avoid mutating the caller's dictionary.
    * Only keys that already exist in `employee_data` are allowed; attempts
      to add new fields raise an error.  This prevents accidental schema
      changes via user input.
    """
    # ----------------------------------------------------------------------- #
    # Input validation
    # ----------------------------------------------------------------------- #
    if not isinstance(employee_data, dict):
        raise TypeError("employee_data must be a dictionary")
    if not isinstance(changes, dict):
        raise TypeError("changes must be a dictionary")

    # ----------------------------------------------------------------------- #
    # Enforce field modification policy
    # ----------------------------------------------------------------------- #
    for key in changes:
        if key not in employee_data:
            raise ValueError(f"Attempt to modify non‑existent field '{key}'")

        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"User lacks permission to modify field '{key}'"
            )

    # ----------------------------------------------------------------------- #
    # Apply changes
    # ----------------------------------------------------------------------- #
    updated = copy.deepcopy(employee_data)
    updated.update(changes)

    return updated