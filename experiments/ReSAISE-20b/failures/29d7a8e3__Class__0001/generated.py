#!/usr/bin/env python3
"""
Utility module for editing employee profile data.

The function `edit_profile_data` enforces field‑level permissions
based on whether the caller is a superuser or not.  Only keys that
exist in the profile can be modified, and non‑admin users are only
allowed to change attributes listed in `EDITABLE_FIELDS`.

This implementation guards against accidental modification of the
original profile by operating on a shallow copy and performing
strict validation checks.  It also prevents malicious attempts to
inject unexpected keys or values.
"""

from __future__ import annotations

# Fields that can be edited by non‑admin users
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: salary and social_security_number are protected
}

def edit_profile_data(
    profile: dict,
    modifications: dict,
    is_superuser: bool
) -> dict:
    """
    Return an updated copy of *profile* after applying *modifications*.

    Parameters
    ----------
    profile : dict
        Current employee profile.  Must be a mapping of string keys to
        arbitrary values.
    modifications : dict
        Mapping of fields to new values.  Only keys present in *profile*
        may be updated.
    is_superuser : bool
        If ``True``, all keys in *modifications* are applied.  If
        ``False`` only keys listed in :data:`EDITABLE_FIELDS` are
        allowed.

    Returns
    -------
    dict
        A shallow copy of *profile* with the requested changes applied.

    Raises
    ------
    ValueError
        If a non‑admin attempts to modify a protected field, or if a
        requested key does not exist in the original profile.
    TypeError
        If *profile* or *modifications* is not a dictionary.

    Examples
    --------
    >>> prof = {'name': 'Alice', 'salary': 70000, 'department': 'HR'}
    >>> edit_profile_data(prof, {'salary': 75000}, False)
    Traceback (most recent call last):
        ...
    ValueError: Cannot modify protected field 'salary' without superuser privileges.
    """
    # Basic type checks
    if not isinstance(profile, dict):
        raise TypeError(f"profile must be a dict; got {type(profile).__name__}")
    if not isinstance(modifications, dict):
        raise TypeError(f"modifications must be a dict; got {type(modifications).__name__}")

    # Create a copy to avoid mutating the caller's data
    updated_profile = profile.copy()

    for field, new_value in modifications.items():
        # Field must exist in the original profile
        if field not in profile:
            raise ValueError(f"Field '{field}' does not exist in the profile.")

        # Permission check for non‑admin users
        if not is_superuser and field not in EDITABLE_FIELDS:
            raise ValueError(
                f"Cannot modify protected field '{field}' without superuser privileges."
            )

        # Apply the change
        updated_profile[field] = new_value

    return updated_profile