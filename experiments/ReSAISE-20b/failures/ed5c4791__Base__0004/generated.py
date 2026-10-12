# -*- coding: utf-8 -*-
"""
Secure employee data modification module.

This module defines the `modify_employee_data` function, which safely updates
employee dictionaries while enforcing strict controls on editable fields.

Security note:
The implementation follows the guidance for CWE‑915 (Improperly Controlled
Modification of Dynamically-Determined Object Attributes) by limiting the set
of attributes that can be modified for non‑admin users. Admin users are
allowed to modify any attribute, but the function still validates input
types and existence of attributes in the target dictionary.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# Global set of fields that regular users are allowed to modify.
EDITABLE_FIELDS: Set[str] = {"name", "position", "department"}


def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Safely modify an employee dictionary.

    Parameters
    ----------
    worker : dict
        Dictionary containing the current attributes of an employee.
    alterations : dict
        Proposed modifications to apply. Keys are attribute names, values
        are the new values.
    admin_privileges : bool
        If True, the caller has administrative rights and may modify any
        attribute. If False, only keys in `EDITABLE_FIELDS` are accepted.

    Returns
    -------
    dict
        A new dictionary representing the updated employee record.

    Raises
    ------
    TypeError
        If `worker` or `alterations` are not dictionaries.
    KeyError
        If a requested key does not exist in `worker`.
    ValueError
        If a non‑admin attempts to modify a protected field.
    """
    if not isinstance(worker, dict):
        raise TypeError("`worker` must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("`alterations` must be a dictionary")

    # Work on a shallow copy to avoid mutating the original input.
    updated_worker = copy.deepcopy(worker)

    for field, new_value in alterations.items():
        # Ensure the field exists on the worker; otherwise raise an error.
        if field not in worker:
            raise KeyError(f"Field '{field}' does not exist on the employee record")

        # Enforce field restrictions for non‑admin users.
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify the field '{field}'. "
                "Only editable fields are allowed: "
                f"{', '.join(sorted(EDITABLE_FIELDS))}"
            )

        # Apply the update.
        updated_worker[field] = new_value

    return updated_worker