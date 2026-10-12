# -*- coding: utf-8 -*-
"""
Employee profile editing utility.

The function `edit_profile_data` safely updates a profile dictionary
according to the rules below:

* Non‑superusers may only modify keys listed in `EDITABLE_FIELDS`.
* Superusers can modify any key that already exists in the profile.
* Keys that are not present in the original profile are rejected to
  avoid accidental creation of new attributes.
* The function returns a **new** dictionary containing the updated
  values; the original `profile` object is left unchanged.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add any other fields that should be editable by normal users.
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return a new profile dictionary with specified modifications applied.

    Parameters
    ----------
    profile : dict
        The original employee profile.
    modifications : dict
        Keys and values to be applied to the profile.
    is_superuser : bool
        Flag indicating whether the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated profile data.

    Raises
    ------
    ValueError
        If a modification attempts to change a non‑editable field,
        or if a key does not exist in the original profile.
    """
    # Validate input types early
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")
    if not isinstance(is_superuser, bool):
        raise TypeError("is_superuser must be a boolean")

    # Prepare the new profile as a shallow copy of the original
    updated_profile = dict(profile)

    for key, new_value in modifications.items():
        # Ensure the field exists in the original profile
        if key not in profile:
            raise ValueError(f"Field '{key}' does not exist in the profile")

        # Enforce edit permissions
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"User lacks permission to modify field '{key}'"
            )

        # Apply the change
        updated_profile[key] = new_value

    return updated_profile

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample profile
    employee = {
        "name": "Alice Smith",
        "position": "Developer",
        "salary": 85000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempting to change the salary (should fail)
    try:
        edit_profile_data(
            employee,
            {"salary": 90000},
            is_superuser=False
        )
    except ValueError as exc:
        print(f"Expected error: {exc}")

    # Admin changing the salary (should succeed)
    updated = edit_profile_data(
        employee,
        {"salary": 90000},
        is_superuser=True
    )
    print("Updated profile:", updated)