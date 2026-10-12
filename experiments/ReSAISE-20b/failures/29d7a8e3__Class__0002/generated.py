# -*- coding: utf-8 -*-
"""
Utility module for editing employee profile data.

The module defines a single public function `edit_profile_data` which safely updates
employee profiles while respecting role‑based permissions.  It guards against
CWE‑913 by ensuring that only explicitly allowed fields can be modified.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Global constants
# --------------------------------------------------------------------------- #

#: Fields that a non‑admin (regular user) is allowed to edit.
EDITABLE_FIELDS = {"name", "position", "department"}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class ProfileUpdateError(ValueError):
    """Raised when an update operation is invalid or disallowed."""
    pass

# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Return a new profile dictionary with requested modifications applied.

    Parameters
    ----------
    profile : dict
        The current employee profile.
    modifications : dict
        Mapping of field names to new values.
    is_superuser : bool
        ``True`` if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.

    Raises
    ------
    ProfileUpdateError
        If a modification attempts to change a protected field without proper
        permissions, or if an unknown field is requested.

    Notes
    -----
    * The function does **not** modify the original ``profile`` dictionary.
    * Only keys present in ``modifications`` are considered; other fields remain
      unchanged.
    * The implementation uses a shallow copy of the profile.  If any values are
      mutable objects (e.g., lists or nested dicts), they are shared between
      the original and the returned profile.  This is intentional to avoid
      unnecessary deep copying of potentially large structures.
    """

    # Validate input types early for clearer error messages
    if not isinstance(profile, dict):
        raise ProfileUpdateError("`profile` must be a dictionary.")
    if not isinstance(modifications, dict):
        raise ProfileUpdateError("`modifications` must be a dictionary.")
    if not isinstance(is_superuser, bool):
        raise ProfileUpdateError("`is_superuser` must be a boolean.")

    # Create a shallow copy to avoid side‑effects on the caller's data
    updated_profile = copy.copy(profile)

    # Define a set of all allowed fields for the current role
    if is_superuser:
        allowed_fields = set(profile.keys()) | EDITABLE_FIELDS
    else:
        allowed_fields = EDITABLE_FIELDS

    # Iterate over requested modifications and apply them if permitted
    for field, new_value in modifications.items():
        if field not in allowed_fields:
            raise ProfileUpdateError(
                f"Field '{field}' cannot be modified by this user."
            )
        updated_profile[field] = new_value

    return updated_profile