#!/usr/bin/env python3
"""
Employee data modification module.

This module provides a single function, `modify_employee_data`, which updates
the attributes of an employee represented as a dictionary.  Regular users are
only allowed to modify a predefined set of fields, while administrators may
modify any field.

The function performs defensive checks to avoid accidental modification of
sensitive data and to guard against common programming pitfalls such as
uncontrolled mutation or accidental infinite loops.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration: fields that non‑admin users are allowed to edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
}

# --------------------------------------------------------------------------- #
# Exception types
# --------------------------------------------------------------------------- #
class EmployeeModificationError(Exception):
    """Raised when a modification request is invalid or not permitted."""


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Update an employee's data with the provided alterations.

    Parameters
    ----------
    worker : dict
        Dictionary containing the employee's current attributes.
    alterations : dict
        Proposed changes to apply. Keys are attribute names; values are the new values.
    admin_privileges : bool
        If ``True`` the caller is an administrator and may modify any field.
        If ``False`` only fields listed in :data:`EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data. The original
        ``worker`` dictionary is **not** modified.

    Raises
    ------
    EmployeeModificationError
        If an alteration attempts to modify a disallowed field for the current
        privilege level, or if the input dictionaries are not of the expected type.
    """

    # Input validation
    if not isinstance(worker, dict):
        raise EmployeeModificationError("`worker` must be a dictionary.")
    if not isinstance(alterations, dict):
        raise EmployeeModificationError("`alterations` must be a dictionary.")
    if not isinstance(admin_privileges, bool):
        raise EmployeeModificationError("`admin_privileges` must be a boolean.")

    # Create a shallow copy to avoid mutating the caller's data.
    updated_worker = copy.deepcopy(worker)

    # Process each alteration
    for field, new_value in alterations.items():
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise EmployeeModificationError(
                f"Field '{field}' cannot be modified without admin privileges."
            )
        # Optional: Add type checks or value validation here if needed.
        updated_worker[field] = new_value

    return updated_worker


# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to run)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Sample employee record
    emp = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin tries to change salary (should fail)
    try:
        modify_employee_data(emp, {"salary": 80000}, admin_privileges=False)
    except EmployeeModificationError as e:
        print(f"Permission error: {e}")

    # Admin changes salary
    updated_emp = modify_employee_data(emp, {"salary": 80000}, admin_privileges=True)
    print("Updated employee:", updated_emp)