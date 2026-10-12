#!/usr/bin/env python3
"""
Utility to safely edit employee profile data.

The function `edit_profile_data` updates a profile dictionary with
the provided modifications. Non‑superusers are limited to editing only
the fields listed in the global `EDITABLE_FIELDS` constant. Any attempt
to modify disallowed fields results in a ValueError.

The implementation guards against accidental mutation of the original
profile and validates inputs to avoid CWE‑913 style vulnerabilities.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Define which fields a normal user may edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # The following fields are intentionally omitted:
    #   - salary
    #   - social_security_number
}


def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new profile dictionary with the requested modifications applied.

    Parameters
    ----------
    profile : dict
        Current employee profile.
    modifications : dict
        Fields to update and their new values.
    is_superuser : bool
        If True, the caller has permission to edit all fields.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a field not in
        `EDITABLE_FIELDS`.
    KeyError
        If a modification references a key that does not exist in the profile.
    TypeError
        If `profile` or `modifications` is not a mapping type.

    Notes
    -----
    - The original `profile` dictionary is never mutated.
    - The function performs a shallow copy; nested mutable objects are
      shared between the original and returned profile.  If deep copies
      are required, adjust `copy.copy` to `copy.deepcopy`.
    """
    # Basic type validation
    if not isinstance(profile, dict):
        raise TypeError(f"profile must be a dict, got {type(profile).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(
            f"modifications must be a dict, got {type(modifications).__name__}"
        )

    # Shallow copy to avoid mutating the original
    new_profile = copy.copy(profile)

    for key, value in modifications.items():
        # Check that the field exists in the original profile
        if key not in profile:
            raise KeyError(f"Field '{key}' does not exist in the profile.")

        # Enforce edit permissions
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑superuser cannot edit the field '{key}'. "
                "Allowed fields: {sorted(EDITABLE_FIELDS)}"
            )

        # Apply the modification
        new_profile[key] = value

    return new_profile


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     current_profile = {
#         "name": "Alice",
#         "position": "Developer",
#         "salary": 90000,
#         "department": "Engineering",
#         "social_security_number": "123-45-6789",
#     }
#
#     mods = {"salary": 95000, "department": "Research"}
#     # Non‑admin attempt
#     try:
#         edit_profile_data(current_profile, mods, is_superuser=False)
#     except ValueError as e:
#         print(e)  # Expected: cannot edit 'salary'
#
#     # Admin attempt
#     updated = edit_profile_data(current_profile, mods, is_superuser=True)
#     print(updated)