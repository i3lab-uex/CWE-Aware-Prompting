#!/usr/bin/env python3
"""
Utility for safely adjusting employee details.

This module defines a single function `adjust_employee_details` that
updates an employee profile dictionary while enforcing permission checks.
It protects sensitive fields from being altered by non‑admin users and
prevents accidental mutation of the original profile.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# -------------------------------------------------------------
# Global constants
# -------------------------------------------------------------

# Fields that a non‑admin user is allowed to modify.
EDITABLE_FIELDS = {"name", "position", "department", "email"}

# Fields that are considered sensitive and can only be modified by admins.
SENSITIVE_FIELDS = {"salary", "social_security_number"}

# -------------------------------------------------------------
# Core function
# -------------------------------------------------------------

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested changes applied.

    Parameters
    ----------
    person : dict
        The original employee profile. Keys represent attribute names.
    alterations : dict
        Mapping of fields to new values that should be applied to the profile.
    has_admin_rights : bool
        True if the caller has administrative privileges; otherwise False.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a sensitive field.
    """
    # Make a shallow copy so that the original `person` is not mutated.
    updated = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Check if the user is allowed to modify this field
        if not has_admin_rights:
            # Non-admins can only touch editable fields.
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify the field '{field}'."
                )
        else:
            # Admins may modify any field, but we still guard against
            # accidental removal of essential keys.
            if field not in person:
                raise ValueError(
                    f"Field '{field}' does not exist in the employee profile."
                )

        # Apply the change
        updated[field] = new_value

    return updated


# -------------------------------------------------------------
# Example usage (for testing only)
# -------------------------------------------------------------
if __name__ == "__main__":
    sample_profile = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
        "email": "alice@example.com",
    }

    # Non‑admin attempting to change position and salary
    try:
        new_profile = adjust_employee_details(
            person=sample_profile,
            alterations={"position": "Senior Developer", "salary": 90000},
            has_admin_rights=False,
        )
    except ValueError as exc:
        print(f"Permission error: {exc}")

    # Admin updating salary
    updated_profile = adjust_employee_details(
        person=sample_profile,
        alterations={"salary": 90000},
        has_admin_rights=True,
    )
    print(updated_profile)