#!/usr/bin/env python3
"""
Employee profile adjustment utility.

This module defines a single function, `adjust_employee_details`, which updates
an employee profile dictionary based on supplied alterations while enforcing
strict access controls to prevent unauthorized changes.

Key security considerations:
- Only a predefined whitelist of editable fields is allowed for non-admin users.
- Sensitive attributes (e.g. `social_security_number`) are protected and
  require admin privileges.
- Attempts to modify unknown or disallowed fields raise a ValueError,
  preventing accidental or malicious updates (CWE-915 mitigation).
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# Whitelisted fields that non-admin users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: salary is omitted from EDITABLE_FIELDS; only admins can change it.
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool
) -> Dict[str, Any]:
    """
    Update an employee profile with the provided alterations.

    Parameters
    ----------
    person : dict
        Current employee profile. Keys are attribute names.
    alterations : dict
        Desired updates. Keys must be a subset of the profile's keys.
    has_admin_rights : bool
        If True, all fields can be updated. If False, only those in
        `EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If an alteration attempts to modify a non-existent field or a
        disallowed field for the current user role.
    """
    # Defensive copy to avoid mutating input
    updated_profile = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Field existence check
        if field not in person:
            raise ValueError(f"Attempted to modify unknown field: '{field}'")

        # Permission check
        if not has_admin_rights:
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Non‑admin users cannot modify field: '{field}'"
                )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_profile = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 85000,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non-admin attempting to change name and salary
    try:
        new_profile = adjust_employee_details(
            person=sample_profile,
            alterations={"name": "Alice Johnson", "salary": 90000},
            has_admin_rights=False
        )
    except ValueError as e:
        print(f"Permission error: {e}")

    # Admin updating salary
    new_profile = adjust_employee_details(
        person=sample_profile,
        alterations={"salary": 90000},
        has_admin_rights=True
    )
    print("Updated profile:", new_profile)