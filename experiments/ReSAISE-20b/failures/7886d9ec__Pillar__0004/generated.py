#!/usr/bin/env python3
"""
Employee profile adjustment module.

The `adjust_employee_details` function updates an employee dictionary
with a set of alterations while enforcing permission checks.

CWE-664 consideration:
The function never leaks or improperly exposes sensitive resources.
All changes are performed on a shallow copy of the original profile
to avoid unintended side‑effects. No external resources are opened or
left dangling.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration: fields that non‑admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add more fields here if needed
}

# --------------------------------------------------------------------------- #
def adjust_employee_details(
    person: dict,
    alterations: dict,
    has_admin_rights: bool
) -> dict:
    """
    Return an updated employee profile dictionary.

    Parameters
    ----------
    person : dict
        The current employee profile.
    alterations : dict
        Keys and new values to be applied.
    has_admin_rights : bool
        True if the caller is an administrator.

    Returns
    -------
    dict
        A new dictionary with the requested updates applied.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field.
    TypeError
        If the input arguments are not of expected types.
    """
    # Basic type checks
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Create a shallow copy to avoid mutating the original
    updated_person = person.copy()

    for field, new_value in alterations.items():
        # If the caller is not an admin, enforce edit restrictions
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Permission denied: cannot modify '{field}' without admin rights"
            )
        # Apply the change
        updated_person[field] = new_value

    return updated_person


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Example usage and simple test
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    # Non-admin attempt to change a protected field
    try:
        adjust_employee_details(
            employee,
            {"salary": 90000},
            has_admin_rights=False
        )
    except ValueError as e:
        print(e)  # Expected: Permission denied

    # Admin changing sensitive data
    updated = adjust_employee_details(
        employee,
        {"salary": 90000, "social_security_number": "987-65-4321"},
        has_admin_rights=True
    )
    print(updated)