#!/usr/bin/env python3
"""
Secure employee profile editing module.

This module defines a single public function `edit_profile_data` that safely updates
employee profiles.  The implementation follows the *CWE‑915* recommendation of
controlling which attributes may be modified dynamically.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile.  Must be a mapping of string keys to any values.
    modifications : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative rights and may modify any field.

    Returns
    -------
    dict
        A new dictionary containing the updated profile data.  The original
        ``profile`` is left untouched.

    Raises
    ------
    PermissionError
        If a non‑superuser attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    ValueError
        If the ``modifications`` argument contains keys that are not present in
        ``profile``.  This guards against accidental creation of new attributes.
    """

    # Ensure we are not mutating the original profile
    updated_profile = copy.deepcopy(profile)

    for key, new_value in modifications.items():
        # Verify that the field exists in the original profile
        if key not in profile:
            raise ValueError(f"Attempted to modify unknown field '{key}'")

        # Restrict non‑admin users to the predefined editable fields
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin user cannot modify the field '{key}'."
            )

        # Apply the change
        updated_profile[key] = new_value

    return updated_profile


# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to edit.
# These should be kept in sync with the application's UI/validation layer
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add additional safe-to-edit fields here
}

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    sample_profile = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    changes = {
        "position": "Senior Developer",
        "salary": 80000,          # Not editable by non-admin
    }

    try:
        print("Non‑admin attempt:")
        new_profile = edit_profile_data(sample_profile, changes, is_superuser=False)
        print(new_profile)
    except Exception as e:
        print(f"Error: {e}")

    try:
        print("\nAdmin attempt:")
        new_profile = edit_profile_data(sample_profile, changes, is_superuser=True)
        print(new_profile)
    except Exception as e:
        print(f"Error: {e}")