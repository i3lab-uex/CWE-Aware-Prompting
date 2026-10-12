# -*- coding: utf-8 -*-
"""
User attribute updater.

This module defines a single public function `update_user_attributes` that
updates a user dictionary with new values while ensuring only attributes
listed in the global `VALID_ATTRIBUTES` set can be modified.  The function
is deliberately defensive: it validates keys, avoids modifying the original
dictionary unless necessary, and raises a `ValueError` for any attempt to
change an unsupported attribute.

CWE-915 mitigation: The function only allows a pre‑defined set of keys to be
modified, preventing an attacker from arbitrarily altering any field in the
user object.
"""

from __future__ import annotations

from typing import Dict, Any

# Global set of attributes that may be updated.
VALID_ATTRIBUTES = {"name", "email", "age"}


def update_user_attributes(user: Dict[str, Any], data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Update user attributes safely.

    Parameters
    ----------
    user : dict
        The original user dictionary.  It may contain arbitrary keys.
    data : dict
        Dictionary of attributes to update.

    Returns
    -------
    dict
        The updated user dictionary.  The input `user` is modified in place.

    Raises
    ------
    ValueError
        If any key in `data` is not present in `VALID_ATTRIBUTES`.
    TypeError
        If `user` or `data` is not a dictionary.
    """
    if not isinstance(user, dict):
        raise TypeError(f"user must be a dict, got {type(user).__name__}")
    if not isinstance(data, dict):
        raise TypeError(f"data must be a dict, got {type(data).__name__}")

    for key, value in data.items():
        if key not in VALID_ATTRIBUTES:
            raise ValueError(f"Attempted to modify invalid attribute: {key!r}")
        user[key] = value

    return user