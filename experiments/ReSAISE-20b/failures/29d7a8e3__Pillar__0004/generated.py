#!/usr/bin/env python3
"""
Employee profile editor.

The module exposes a single function, :func:`edit_profile_data`, which
updates an employee profile dictionary with the supplied modifications.
Only a predefined set of fields may be edited by non‑admin users.  Superusers
may modify any field.

The implementation takes care to avoid accidental mutation of the caller’s
dictionary by working on a shallow copy.  It also validates that all keys in
``modifications`` are legitimate fields of the profile; any unknown key causes
a :class:`ValueError`.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any, Iterable

# Fields that a non‑admin user is allowed to edit.
EDITABLE_FIELDS: Iterable[str] = ("name", "position", "department")

def _validate_modifications(profile: Dict[str, Any], modifications: Dict[str, Any]) -> None:
    """
    Ensure that all keys in ``modifications`` exist in the original profile.
    Raise :class:`ValueError` if any key is missing.

    Parameters
    ----------
    profile :
        The original employee profile dictionary.
    modifications :
        Dictionary of proposed changes.

    Raises
    ------
    ValueError
        If a key in ``modifications`` is not present in ``profile``.
    """
    unknown_keys = set(modifications) - set(profile)
    if unknown_keys:
        raise ValueError(f"Attempted to modify unknown fields: {unknown_keys}")

def _is_field_editable(field_name: str, is_superuser: bool) -> bool:
    """
    Determine whether a field can be edited by the caller.

    Parameters
    ----------
    field_name :
        Name of the profile field.
    is_superuser :
        ``True`` if caller has admin privileges.

    Returns
    -------
    bool
        ``True`` if the field may be edited, otherwise ``False``.
    """
    return is_superuser or field_name in EDITABLE_FIELDS

def edit_profile_data(
    profile: Dict[str, Any],
    modifications: Dict[str, Any],
    is_superuser: bool,
) -> Dict[str, Any]:
    """
    Edit an employee profile dictionary with supplied modifications.

    Parameters
    ----------
    profile :
        The current employee profile as a dictionary.
    modifications :
        Dictionary of fields to be updated with new values.
    is_superuser :
        ``True`` if the operation is performed by an admin user.

    Returns
    -------
    Dict[str, Any]
        A new dictionary containing the updated profile.  The original
        ``profile`` remains unchanged.

    Raises
    ------
    ValueError
        If the caller attempts to modify a field that is not editable,
        or if ``modifications`` contains keys that are absent from
        ``profile``.

    Notes
    -----
    * The function performs a shallow copy of the profile to avoid side‑effects.
    * Sensitive fields (e.g. ``social_security_number``) are protected from
      accidental modification by non‑admin users.
    """
    # Validate that all keys exist in the original profile
    _validate_modifications(profile, modifications)

    # Create a shallow copy so that the original profile is not mutated
    updated_profile = copy.copy(profile)

    for key, new_value in modifications.items():
        if not _is_field_editable(key, is_superuser):
            raise ValueError(
                f"Field '{key}' cannot be edited by non‑admin users."
            )
        updated_profile[key] = new_value

    return updated_profile