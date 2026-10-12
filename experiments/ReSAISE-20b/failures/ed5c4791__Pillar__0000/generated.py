# -*- coding: utf-8 -*-
"""
Employee data modification module.

The function `modify_employee_data` updates an employee dictionary based on
the supplied alterations. Regular users may only modify fields listed in
`EDITABLE_FIELDS`. Administrators can change any field.

CWE-664 (Improper Control of a Resource Through its Lifetime) is mitigated
by ensuring that the employee dictionary is copied before any changes are
applied, preventing accidental mutation of shared resources.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}


def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool = False,
) -> Dict[str, Any]:
    """
    Update an employee dictionary with the supplied alterations.

    Parameters
    ----------
    worker : dict
        The original employee data.
    alterations : dict
        Proposed changes to apply.
    admin_privileges : bool, optional
        If True, the caller has administrative rights and can modify any field.
        Default is False.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in `EDITABLE_FIELDS`.
    TypeError
        If any argument is of an unexpected type.
    """
    # Basic type checks to guard against accidental misuse
    if not isinstance(worker, dict):
        raise TypeError("worker must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(admin_privileges, bool):
        raise TypeError("admin_privileges must be a boolean")

    # Work on a shallow copy to avoid mutating the original dictionary
    updated_worker = copy.deepcopy(worker)

    # Determine which keys are allowed to be altered
    if admin_privileges:
        allowed_keys = set(updated_worker.keys()).union(alterations.keys())
    else:
        allowed_keys = EDITABLE_FIELDS

    # Apply alterations, validating permissions
    for key, value in alterations.items():
        if key not in allowed_keys:
            raise ValueError(
                f"Unauthorized modification of field '{key}'. "
                "Only editable fields can be changed by regular users."
            )
        updated_worker[key] = value

    return updated_worker