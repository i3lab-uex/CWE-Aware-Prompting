#!/usr/bin/env python3
"""
Employee profile update utility.

This module provides a single public function `adjust_employee_details` which
returns an updated employee profile dictionary after applying the requested
alterations.  The function enforces a strict whitelist of editable fields for
non‑admin users, raising an exception if a user attempts to modify a protected
field.  It also protects against accidental mutation of the original profile
by operating on a shallow copy.

Author: ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Configuration – editable fields for non‑admin users
# --------------------------------------------------------------------------- #
EDITABLE_FIELDS = {"name", "position", "department"}


# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #
class InvalidFieldError(ValueError):
    """Raised when an alteration references a field that does not exist."""
    pass


class PermissionDeniedError(PermissionError):
    """Raised when a non‑admin attempts to modify a protected field."""
    pass


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def adjust_employee_details(
    person: Dict[str, Any],
    alterations: Dict[str, Any],
    has_admin_rights: bool,
) -> Dict[str, Any]:
    """
    Return an updated employee profile dictionary.

    Parameters
    ----------
    person : dict
        Current employee profile.  Keys may include any of the following:
            - name (str)
            - position (str)
            - salary (float)
            - department (str)
            - social_security_number (str)

    alterations : dict
        Dictionary of field names to new values that should be applied.

    has_admin_rights : bool
        If ``True`` the caller is an administrator and may modify any field.
        Otherwise, only fields listed in ``EDITABLE_FIELDS`` are permitted.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.  The input
        ``person`` is not modified.

    Raises
    ------
    InvalidFieldError
        If an alteration references a key that does not exist in the original
        profile.

    PermissionDeniedError
        If a non‑admin attempts to modify a protected field.
    """
    # Validate input types
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Create a shallow copy to avoid mutating the original profile
    updated_profile = copy.deepcopy(person)

    for key, new_value in alterations.items():
        # Ensure the field exists
        if key not in person:
            raise InvalidFieldError(f"Field '{key}' does not exist in the profile")

        # Enforce non‑admin edit restrictions
        if not has_admin_rights and key not in EDITABLE_FIELDS:
            raise PermissionDeniedError(
                f"Non‑admin users cannot modify the field '{key}'"
            )

        # Apply the alteration
        updated_profile[key] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Example usage (uncomment to run as a script)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    example_profile = {
        "name": "Alice Smith",
        "position": "Engineer",
        "salary": 95000.0,
        "department": "R&D",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin attempt to change salary (should raise PermissionDeniedError)
    try:
        new_profile = adjust_employee_details(
            person=example_profile,
            alterations={"salary": 100000},
            has_admin_rights=False,
        )
    except PermissionDeniedError as e:
        print(f"Permission error: {e}")

    # Admin updates salary and SSN
    admin_profile = adjust_employee_details(
        person=example_profile,
        alterations={"salary": 100000, "social_security_number": "987-65-4321"},
        has_admin_rights=True,
    )
    print(admin_profile)