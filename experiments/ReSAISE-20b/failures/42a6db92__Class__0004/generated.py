# -*- coding: utf-8 -*-
"""
Utility module for managing user privilege levels.

This module contains a single function `modify_privilege_level` that allows an
administrator to change the privilege level of another user account.  The function
performs proper authorization checks, validates input values, and updates the
in-memory `USERS` dictionary accordingly.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Example USERS dictionary.  In a real application this would be replaced by
# persistent storage (e.g., a database).
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice",   "role": "admin",     "privilege_level": "admin"},
    2: {"name": "Bob",     "role": "moderator", "privilege_level": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege_level": "normal"},
    # ... additional users ...
}

# Allowed privilege levels.
ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(
    acting_user_id: int,
    user_id_to_change: int,
    new_level: str
) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to make the change.
    user_id_to_change : int
        The ID of the target user whose privilege level will be modified.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change was applied, False otherwise.

    Notes
    -----
    * The function checks that the acting user exists and has an 'admin'
      role.  This mitigates CWE-862 (Missing Authorization).
    * The target user must exist; otherwise the function returns False.
    * `new_level` is validated against a whitelist to avoid injection of
      unexpected values.
    * The function does not allow an admin to demote themselves; this is a
      defensive measure against accidental lock‑out.
    """
    # Verify that the acting user exists and is an admin.
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist.
        return False
    if acting_user.get("role") != "admin":
        # Acting user is not authorized to change privileges.
        return False

    # Prevent self‑demotion: an admin should not lower their own privilege.
    if acting_user_id == user_id_to_change:
        return False

    # Validate the target user exists.
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Validate the requested new privilege level.
    if new_level not in ALLOWED_LEVELS:
        return False

    # Apply the change.
    target_user["privilege_level"] = new_level
    # Optionally keep the role in sync with privilege level for simplicity.
    target_user["role"] = new_level

    return True