#!/usr/bin/env python3
"""
Employee data modification module.

This module defines the `modify_employee_data` function, which safely updates
employee attributes based on the caller's privilege level. It protects against
CWE-915 by strictly controlling which fields can be altered when the caller is
not an administrator.
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration – fields that regular users are allowed to edit.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # Add other fields that should be editable by non‑admin users here.
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def modify_employee_data(
    worker: Dict[str, Any],
    alterations: Dict[str, Any],
    admin_privileges: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee dictionary after applying allowed alterations.

    Parameters
    ----------
    worker : dict
        Current employee record. Must be a mapping of string keys to any values.
    alterations : dict
        Proposed changes, mapping attribute names to new values.
    admin_privileges : bool
        If ``True``, the caller may modify any field. Otherwise only fields in
        :data:`EDITABLE_FIELDS` are accepted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee data.

    Raises
    ------
    TypeError
        If any of the arguments is not a dictionary.
    ValueError
        If an attempt is made to modify a protected field without admin
        privileges.
    """
    # --------------------------------------------------------------------- #
    # Validate input types to avoid accidental injection of non‑dict objects.
    # --------------------------------------------------------------------- #
    if not isinstance(worker, dict):
        raise TypeError("`worker` must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("`alterations` must be a dictionary")
    if not isinstance(admin_privileges, bool):
        raise TypeError("`admin_privileges` must be a boolean")

    # --------------------------------------------------------------------- #
    # Create a shallow copy so we do not mutate the original worker dict.
    # --------------------------------------------------------------------- #
    updated_worker = copy.deepcopy(worker)

    # --------------------------------------------------------------------- #
    # Iterate over the proposed alterations.
    # --------------------------------------------------------------------- #
    for field, new_value in alterations.items():
        # Reject any keys that are not plain strings (prevents "__dict__" etc.)
        if not isinstance(field, str):
            raise ValueError(f"Ignoring non‑string field name: {field!r}")

        # Skip any keys that are not present in the worker – we do not allow
        # creating new attributes arbitrarily.
        if field not in worker:
            raise ValueError(f"Field {field!r} does not exist on the employee record")

        # Enforce editability rules
        if not admin_privileges and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field {field!r}"
            )

        # Apply the alteration
        updated_worker[field] = new_value

    return updated_worker


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"salary": 95000, "department": "Product"}

    try:
        # Non‑admin attempt
        print(modify_employee_data(employee, changes, admin_privileges=False))
    except ValueError as exc:
        print(f"Non‑admin error: {exc}")

    # Admin attempt
    updated = modify_employee_data(employee, changes, admin_privileges=True)
    print("Admin update:", updated)