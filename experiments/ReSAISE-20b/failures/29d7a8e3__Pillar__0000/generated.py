# -*- coding: utf-8 -*-
"""
Utility to safely edit employee profile data.

The function `edit_profile_data` enforces that non‑admin users can only modify
fields listed in the global constant `EDITABLE_FIELDS`.  Attempts to change
other fields raise a ValueError.  The function returns a new dictionary
containing the updated profile, leaving the original untouched.

The implementation avoids common pitfalls such as mutating the input
dictionary in place and ensures that only existing keys are updated.
"""

from __future__ import annotations

# Global constant: fields that non‑admin users may edit.
EDITABLE_FIELDS = {"name", "position", "department"}

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return a new profile dictionary with the requested modifications applied.

    Parameters
    ----------
    profile : dict
        Current employee profile.
    modifications : dict
        Dictionary mapping field names to new values.
    is_superuser : bool
        Flag indicating whether the caller has administrative privileges.

    Returns
    -------
    dict
        Updated profile dictionary.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a disallowed field.
    KeyError
        If a modification refers to a key that does not exist in the profile.
    """
    # Validate input types
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")
    if not isinstance(is_superuser, bool):
        raise TypeError("is_superuser must be a boolean")

    # Create a shallow copy to avoid mutating the original profile
    updated_profile = dict(profile)

    for field, new_value in modifications.items():
        # Ensure the field exists in the profile
        if field not in updated_profile:
            raise KeyError(f"Field '{field}' does not exist in the profile")

        # Enforce edit permissions
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot modify the field '{field}'"
            )

        # Apply the modification
        updated_profile[field] = new_value

    return updated_profile


# Example usage (for illustration; remove or comment out in production)
if __name__ == "__main__":
    employee = {
        "name": "Jane Doe",
        "position": "Developer",
        "salary": 75000,
        "department": "Engineering",
        "social_security_number": "123-45-6789"
    }

    # Non‑admin attempts to change name and salary
    try:
        new_emp = edit_profile_data(
            profile=employee,
            modifications={"name": "Jane Smith", "salary": 80000},
            is_superuser=False
        )
    except ValueError as e:
        print(f"Permission error: {e}")

    # Admin changes salary
    new_emp = edit_profile_data(
        profile=employee,
        modifications={"salary": 80000},
        is_superuser=True
    )
    print(new_emp)