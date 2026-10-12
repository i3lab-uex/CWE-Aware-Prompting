# -*- coding: utf-8 -*-

"""
Employee profile editing module.

This module provides a single function `edit_profile_data` that updates an
employee profile dictionary according to the supplied modifications.
Non‑admin users are restricted to a predefined set of editable fields
(`EDITABLE_FIELDS`).  The function performs defensive checks to avoid
unintended modifications and to guard against common security pitfalls
such as the inadvertent execution of arbitrary code or modification of
protected attributes.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, List

# Global constant listing the fields that can be edited by non‑admin users.
EDITABLE_FIELDS: List[str] = [
    "name",
    "position",
    "department",
    # Add more fields as needed.
]

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool
) -> Dict[str, Any]:
    """
    Update an employee profile with the supplied modifications.

    Parameters
    ----------
    profile : dict
        Current employee profile.  Keys are attribute names.
    modifications : dict
        Desired changes: key is the field to modify, value is the new value.
    is_superuser : bool
        True if the caller has administrative privileges.

    Returns
    -------
    dict
        A new dictionary containing the updated profile.  The original
        `profile` is not modified.

    Raises
    ------
    ValueError
        If a non‑admin user attempts to modify a field that is not in
        `EDITABLE_FIELDS`, or if the supplied modification key does not
        exist in the original profile.

    Notes
    -----
    * The function performs a shallow copy of the input `profile`.  Nested
      mutable objects are not deep‑cloned; use `copy.deepcopy` if a full
      clone is required.
    * No external code execution or dynamic attribute resolution is
      performed, mitigating CWE‑913 risks.
    """
    if not isinstance(profile, dict):
        raise TypeError("profile must be a dictionary")
    if not isinstance(modifications, dict):
        raise TypeError("modifications must be a dictionary")
    if not isinstance(is_superuser, bool):
        raise TypeError("is_superuser must be a boolean")

    # Create a shallow copy to avoid mutating the caller's dictionary.
    updated_profile = copy.deepcopy(profile)

    for key, new_value in modifications.items():
        # Reject keys that are not present in the original profile.
        if key not in profile:
            raise ValueError(f"Field '{key}' does not exist in the profile")

        # For non‑admin users, enforce editable field restrictions.
        if not is_superuser and key not in EDITABLE_FIELDS:
            raise ValueError(
                f"Field '{key}' is not editable by non‑admin users"
            )

        # Perform the update.
        updated_profile[key] = new_value

    return updated_profile