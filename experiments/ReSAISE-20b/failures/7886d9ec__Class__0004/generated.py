# -*- coding: utf-8 -*-
"""
Employee profile update utility.

This module defines the `adjust_employee_details` function, which safely updates
an employee profile dictionary.  Non‑admin users may only modify fields listed
in the `EDITABLE_FIELDS` constant.  Admins can update any field.

The implementation guards against arbitrary code execution and ensures that
only existing keys are updated.  Invalid field names result in a ValueError.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department"}

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with specified fields updated.

    Parameters
    ----------
    person : dict
        The original employee profile.  Keys are expected to be strings.
    alterations : dict
        Mapping of field names to new values that should replace the current ones.
    has_admin_rights : bool
        ``True`` if the caller is an administrator and may modify any field;
        otherwise only fields in :data:`EDITABLE_FIELDS` are allowed.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.  The original
        ``person`` dictionary is not modified.

    Raises
    ------
    ValueError
        If an alteration attempts to modify a field that the caller is not
        permitted to change, or if the key does not exist in ``person``.
    """
    # Validate input types
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")

    # Work on a shallow copy to avoid mutating the original
    updated_profile = copy.deepcopy(person)

    for key, new_value in alterations.items():
        if not isinstance(key, str):
            raise ValueError(f"Field name must be a string, got {type(key).__name__}")

        if key not in person:
            raise ValueError(f"Field '{key}' does not exist in the employee profile")

        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Insufficient privileges to modify field '{key}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Perform the update
        updated_profile[key] = new_value

    return updated_profile


# Example usage (for manual testing only; remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Developer", "salary": 95000}
    try:
        # Non-admin attempt
        updated = adjust_employee_details(employee, changes, has_admin_rights=False)
        print("Non-admin update succeeded:", updated)
    except ValueError as exc:
        print("Non-admin update failed:", exc)

    try:
        # Admin attempt
        updated = adjust_employee_details(employee, changes, has_admin_rights=True)
        print("Admin update succeeded:", updated)
    except ValueError as exc:
        print("Admin update failed:", exc)