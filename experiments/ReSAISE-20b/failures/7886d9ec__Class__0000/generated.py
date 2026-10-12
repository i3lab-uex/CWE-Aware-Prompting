# -*- coding: utf-8 -*-
"""
Employee profile update utility.

This module defines a single function, `adjust_employee_details`, which updates
an employee profile dictionary with new values.  The update respects the
permission level of the caller: a non‑admin user can only modify fields that
are listed in `EDITABLE_FIELDS`; an admin can update any field.

The function is intentionally defensive: it validates the input types,
ensures that only existing keys are updated, and returns a new dictionary
to avoid accidental mutation of the caller's data.  This mitigates CWE‑913
by preventing uncontrolled modification of dynamically managed objects.
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
    Update an employee profile with the provided alterations.

    Parameters
    ----------
    person : dict
        Current employee profile.  Must be a mapping from string keys to any values.
    alterations : dict
        Dictionary of fields to update.  Keys are field names; values are the new values.
    has_admin_rights : bool
        ``True`` if the caller is an admin and may update any field.
        ``False`` restricts updates to `EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.

    Raises
    ------
    TypeError
        If any argument is not of the expected type.
    ValueError
        If an alteration attempts to modify a non‑existent field for a non‑admin.
    """
    # Validate input types
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Work on a copy to avoid side effects
    updated_person = copy.deepcopy(person)

    for field, new_value in alterations.items():
        if not isinstance(field, str):
            raise TypeError("Field names must be strings")

        # Non‑admin users are limited to editable fields
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'. "
                f"Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Ensure the field exists in the profile
        if field not in updated_person:
            raise ValueError(f"Field '{field}' does not exist in the employee profile")

        # Apply the update
        updated_person[field] = new_value

    return updated_person


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    changes = {"position": "Senior Developer", "salary": 95000}

    try:
        # Non‑admin attempt: should fail for 'salary'
        updated = adjust_employee_details(employee, changes, has_admin_rights=False)
    except ValueError as e:
        print(f"Non‑admin update failed: {e}")

    # Admin attempt: succeeds
    updated_admin = adjust_employee_details(employee, changes, has_admin_rights=True)
    print("Updated profile:", updated_admin)