#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Employee profile updater.

This module provides a single public function `adjust_employee_details` which
updates an employee's profile dictionary with new values while enforcing a
strict whitelist of editable fields for non‑admin users.  The function is
designed to avoid CWE‑915 by ensuring that only explicitly permitted keys
can be modified when the caller does not have administrative rights.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Set


# --------------------------------------------------------------------------- #
# Global configuration: list of fields that can be edited by non‑admin users.
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS: Set[str] = {
    "name",
    "position",
    "department",
    # The following fields are allowed to be updated, but only by admins.
    # They appear here for documentation purposes; the function enforces
    # additional checks based on `has_admin_rights`.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested alterations
    applied.  Only keys listed in `EDITABLE_FIELDS` may be changed by non‑admin
    users.  Admin users may modify any key present in the original profile.

    Parameters
    ----------
    person : dict
        The current employee profile.  It is not modified in place.
    alterations : dict
        Mapping of fields to new values that should be applied to the profile.
    has_admin_rights : bool
        ``True`` if the caller is an administrator; otherwise ``False``.

    Returns
    -------
    dict
        A new dictionary representing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a field not in ``EDITABLE_FIELDS``.
    KeyError
        If an admin attempts to modify a field that does not exist in the
        original profile.  (This protects against typos and accidental schema
        changes.)

    Notes
    -----
    - The function performs a shallow copy of the original dictionary; nested
      structures are not deep‑copied.  If a deeper copy is required, adjust the
      implementation accordingly.
    - The function deliberately rejects any alterations that would add new keys
      not already present in ``person``.  This prevents accidental schema drift.
    """
    # Validate inputs
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Create a shallow copy to avoid mutating the original
    updated_profile = copy.deepcopy(person)

    for field, new_value in alterations.items():
        # Check that the field exists in the original profile
        if field not in person:
            raise KeyError(f"Field '{field}' does not exist in the employee profile")

        if has_admin_rights:
            # Admin users may modify any existing field
            updated_profile[field] = new_value
        else:
            # Non‑admin users may only modify whitelisted fields
            if field not in EDITABLE_FIELDS:
                raise ValueError(
                    f"Unauthorized modification attempt on non‑editable field '{field}'"
                )
            updated_profile[field] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (uncomment to run as a script)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Sample employee profile
    employee = {
        "name": "Jane Doe",
        "position": "Software Engineer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempting to change position (allowed)
    try:
        updated = adjust_employee_details(
            person=employee,
            alterations={"position": "Senior Software Engineer"},
            has_admin_rights=False,
        )
        print("Updated (non‑admin):", updated)
    except Exception as e:
        print(f"Error: {e}")

    # Non‑admin attempting to change salary (disallowed)
    try:
        updated = adjust_employee_details(
            person=employee,
            alterations={"salary": 95000},
            has_admin_rights=False,
        )
    except Exception as e:
        print(f"Error: {e}")

    # Admin changing salary (allowed)
    try:
        updated = adjust_employee_details(
            person=employee,
            alterations={"salary": 95000},
            has_admin_rights=True,
        )
        print("Updated (admin):", updated)
    except Exception as e:
        print(f"Error: {e}")