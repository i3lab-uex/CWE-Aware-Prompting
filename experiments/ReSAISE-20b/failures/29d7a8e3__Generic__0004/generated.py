#!/usr/bin/env python3
"""
Employee profile editing module.

This module defines the `edit_profile_data` function which updates an employee
profile dictionary in a controlled manner. Only fields listed in the global
`EDITABLE_FIELDS` constant may be changed by non‑superusers. Superusers (admin
users) are allowed to modify any field.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that regular users are allowed to modify.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Salary is considered sensitive; only superusers can edit it.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool = False
) -> dict:
    """
    Update an employee profile with the provided modifications.

    Parameters
    ----------
    profile : dict
        The current employee profile. Keys are field names, values are the
        corresponding data.
    modifications : dict
        A dictionary of fields to update with their new values.
    is_superuser : bool, optional
        Flag indicating whether the caller has administrative privileges. If
        ``False`` only fields in :data:`EDITABLE_FIELDS` may be updated.

    Returns
    -------
    dict
        A new dictionary containing the updated profile. The original ``profile``
        is not mutated.

    Raises
    ------
    ValueError
        If a non‑superuser attempts to modify a field not in
        :data:`EDITABLE_FIELDS`.

    Notes
    -----
    * The function performs a shallow copy of ``profile`` before applying any
      changes to avoid side effects.
    * The function does not validate the types or formats of field values; that
      should be handled elsewhere in the application.
    """
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")

    # Create a shallow copy to avoid mutating the original profile.
    updated_profile = dict(profile)

    for field, new_value in modifications.items():
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{field}' cannot be edited by non‑superusers."
            )
        # Apply the update.
        updated_profile[field] = new_value

    return updated_profile