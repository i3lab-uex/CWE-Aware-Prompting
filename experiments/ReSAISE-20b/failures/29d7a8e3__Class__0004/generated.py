#!/usr/bin/env python3
"""
Utility for safely editing employee profile data.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

# ----------------------------------------------------------------------
# Global constant: fields that a non‑admin user is allowed to modify.
# ----------------------------------------------------------------------
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: sensitive fields like salary or social_security_number
    # are intentionally omitted.
}

# ----------------------------------------------------------------------
# Custom exception types
# ----------------------------------------------------------------------
class InvalidFieldError(ValueError):
    """Raised when a non‑admin attempts to modify an uneditable field."""


# ----------------------------------------------------------------------
def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with requested modifications applied.

    Parameters
    ----------
    profile : dict
        Current employee profile. Keys are strings; values can be any JSON‑serialisable type.
    modifications : dict
        Mapping of field names to new values that should be applied to the profile.
    is_superuser : bool
        ``True`` if the caller has administrative privileges and may edit any field.
        ``False`` restricts modifications to the fields listed in :data:`EDITABLE_FIELDS`.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    InvalidFieldError
        If a non‑admin attempts to modify a field that is not in :data:`EDITABLE_FIELDS`.

    Notes
    -----
    * The function does **not** modify the input ``profile`` dictionary in place;
      it returns a new dictionary instance.
    * The function performs a shallow copy of the original profile. If values are
      mutable objects, those objects are shared between the old and new profiles.
    """
    # Defensive copy to avoid mutating caller's data
    updated_profile = copy.deepcopy(profile)

    for field, new_value in modifications.items():
        # If the user is not a superuser, enforce editable field restriction
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise InvalidFieldError(
                f"Non‑admin users cannot modify the field '{field}'."
            )

        # Apply the modification
        updated_profile[field] = new_value

    return updated_profile


# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Example usage and basic test
    original = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 90000,
        "department": "Engineering",
        "social_security_number": "123-45-6789",
    }

    # Non‑admin tries to change position and salary
    try:
        new_profile = edit_profile_data(
            original,
            {"position": "Senior Developer", "salary": 95000},
            is_superuser=False,
        )
    except InvalidFieldError as exc:
        print(f"Error: {exc}")

    # Admin changes salary
    new_profile = edit_profile_data(
        original,
        {"salary": 95000},
        is_superuser=True,
    )
    print("Updated profile:", new_profile)