#!/usr/bin/env python3
"""
Utility for editing employee profile data with permission checks.

The module defines a single public function, `edit_profile_data`, which
updates an employee profile dictionary according to the supplied
modifications.  Only fields listed in `EDITABLE_FIELDS` may be altered by
non‑admin users; superusers (is_superuser=True) can modify any field.
"""

from __future__ import annotations

import copy
from typing import Any, Dict

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS = {
    "name",
    "position",
    "department",
    # Note: salary and social_security_number are protected fields.
}

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Return a new employee profile dictionary with the requested modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile.
    modifications : dict
        Keys are field names, values are the new values to set.
    is_superuser : bool
        If ``True``, all fields may be modified.  If ``False``, only fields
        listed in :data:`EDITABLE_FIELDS` may be changed.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The original ``profile``
        is left untouched.

    Raises
    ------
    ValueError
        If ``modifications`` contains a key that is not allowed for the current
        user level.
    TypeError
        If ``profile`` or ``modifications`` are not mapping types.

    Examples
    --------
    >>> original = {'name': 'Alice', 'salary': 70000, 'department': 'HR'}
    >>> edit_profile_data(original, {'name': 'Alicia'}, False)
    {'name': 'Alicia', 'salary': 70000, 'department': 'HR'}
    >>> edit_profile_data(original, {'salary': 75000}, False)
    Traceback (most recent call last):
        ...
    ValueError: Cannot modify protected field 'salary' for non‑admin user.

    """
    # Validate inputs
    if not isinstance(profile, dict):
        raise TypeError("profile must be a mapping type (dict).")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a mapping type (dict).")

    # Create a shallow copy to avoid mutating the original profile
    updated_profile = copy.deepcopy(profile)

    # Determine allowed fields based on user privilege
    if is_superuser:
        allowed_fields = set(profile.keys()) | set(modifications.keys())
    else:
        allowed_fields = EDITABLE_FIELDS

    # Apply modifications with permission checks
    for key, value in modifications.items():
        if not is_superuser and key not in allowed_fields:
            raise ValueError(
                f"Cannot modify protected field '{key}' for non‑admin user."
            )
        updated_profile[key] = value

    return updated_profile