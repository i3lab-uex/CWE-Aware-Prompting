#!/usr/bin/env python3
"""
Utility to adjust employee profile details with permission checks.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global configuration
# --------------------------------------------------------------------------- #

# These are the only fields that non‑admin users may modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: sensitive fields such as 'salary' or 'social_security_number'
    # are intentionally omitted to prevent unauthorized changes.
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def adjust_employee_details(
    person: dict,
    alterations: dict,
    has_admin_rights: bool
) -> dict:
    """
    Return an updated employee profile dictionary after applying allowed changes.

    Parameters
    ----------
    person : dict
        Current employee profile.
    alterations : dict
        Dictionary of fields to update with new values.
    has_admin_rights : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated employee profile.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a field that is not in
        ``EDITABLE_FIELDS``.
    """
    if not isinstance(person, dict):
        raise TypeError("person must be a dictionary")
    if not isinstance(alterations, dict):
        raise TypeError("alterations must be a dictionary")
    if not isinstance(has_admin_rights, bool):
        raise TypeError("has_admin_rights must be a boolean")

    # Work on a shallow copy to avoid mutating the input.
    updated_person = person.copy()

    for field, new_value in alterations.items():
        # If the user is not an admin and tries to modify a protected field,
        # raise an error.
        if not has_admin_rights and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' is not editable without admin rights."
            )

        # Update the field.  This will add new keys if they did not exist
        # previously, which is intentional for admin users.
        updated_person[field] = new_value

    return updated_person