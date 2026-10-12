#!/usr/bin/env python3
"""
Employee profile editing module.

This module defines a single public function, `edit_profile_data`, which updates
an employee's profile dictionary in place and returns the updated dictionary.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is intentionally omitted to prevent non‑admins from
    # modifying compensation data.
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_modifications(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> None:
    """
    Validate that each modification key exists in the profile and is permitted.

    Raises
    ------
    KeyError
        If a modification key does not exist in the profile.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    """
    for key in modifications:
        if key not in profile:
            raise KeyError(f"Field '{key}' does not exist in the employee profile.")
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise PermissionError(
                f"Non‑admin users cannot modify the field '{key}'."
            )

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Update an employee profile with the provided modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile. The function modifies this dictionary in
        place and also returns it.
    modifications : dict
        Mapping of field names to new values that should be applied to the
        profile.
    is_superuser : bool
        ``True`` if the caller has administrative privileges; otherwise
        ``False``.

    Returns
    -------
    dict
        The updated profile dictionary.

    Raises
    ------
    KeyError
        If a requested modification refers to a field that does not exist in
        the profile.
    PermissionError
        If a non‑admin attempts to modify a protected field.
    """
    # Ensure the inputs are dictionaries
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary.")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary.")

    # Validate modifications before applying them
    _validate_modifications(profile, modifications, is_superuser)

    # Apply the changes
    for key, value in modifications.items():
        profile[key] = value

    return profile