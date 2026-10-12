# -*- coding: utf-8 -*-
"""
Utility for editing employee profile data.

The module defines a single public function `edit_profile_data` that updates
a given employee profile dictionary with new values while respecting
access restrictions. Non‑superusers may only modify fields listed in
`EDITABLE_FIELDS`. Superusers can edit any field present in the profile.

Security considerations:
- The function performs a shallow copy of the original profile to avoid
  accidental mutation.
- Attempts to modify non‑existent fields or disallowed fields raise a
  `ValueError`.
"""

from __future__ import annotations

# Fields that regular users are allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Add other non‑sensitive fields here.
}


def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return a new employee profile dictionary with applied modifications.

    Parameters
    ----------
    profile : dict
        The current employee profile. Must contain keys for all attributes.
    modifications : dict
        Mapping of field names to new values that should be applied.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary with the requested updates applied.

    Raises
    ------
    ValueError
        If a modification references a field that does not exist in the
        original profile or, for non‑superusers, is not listed in
        ``EDITABLE_FIELDS``.
    """
    # Shallow copy to avoid mutating the original profile
    updated_profile = dict(profile)

    for field, new_value in modifications.items():
        if field not in profile:
            raise ValueError(
                f"Field '{field}' does not exist in the employee profile."
            )

        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Non‑admin users cannot edit the field '{field}'."
            )

        updated_profile[field] = new_value

    return updated_profile