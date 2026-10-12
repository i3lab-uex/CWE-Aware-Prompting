#!/usr/bin/env python3
"""
Employee data modification module.

This module defines the function `modify_employee_data` that updates an employee
dictionary while enforcing field‑level permissions.  Regular users may only modify
attributes listed in the global `EDITABLE_FIELDS` set; admins can change any field.

Security considerations:
* A shallow copy of the employee dict is made before applying changes to avoid
  accidental mutation of the original data structure.
* Only keys present in the employee dict are considered; unknown fields raise
  an error to prevent accidental injection of arbitrary data.
* The function checks the type of `admin_privileges` to guard against
  accidental truthy values.
* The implementation is resistant to CWE‑664 by ensuring that the resource
  (the employee dict) remains in a valid state throughout the operation.
"""

from __future__ import annotations

# Fields that can be edited by non‑admin users
EDITABLE_FIELDS = {"name", "position", "department"}

def modify_employee_data(
    worker: dict,
    alterations: dict,
    admin_privileges: bool
) -> dict:
    """
    Update an employee dictionary with the provided alterations.

    Parameters
    ----------
    worker : dict
        Original employee data.  Must contain keys like 'name', 'position',
        'salary', 'department', and 'social_security_number'.
    alterations : dict
        Proposed changes to apply.
    admin_privileges : bool
        True if the caller has administrative rights.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If `admin_privileges` is not a boolean.
    ValueError
        * If an alteration attempts to modify a non‑existent field.
        * If a regular user tries to change a non‑editable field.
    """
    if not isinstance(admin_privileges, bool):
        raise TypeError("admin_privileges must be a boolean")

    # Create a shallow copy to avoid mutating the input dictionary
    updated_worker = worker.copy()

    for key, value in alterations.items():
        if key not in worker:
            raise ValueError(f"Field '{key}' does not exist in employee data")

        # Enforce field restrictions for non‑admins
        if not admin_privileges and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{key}'"
            )

        updated_worker[key] = value

    return updated_worker