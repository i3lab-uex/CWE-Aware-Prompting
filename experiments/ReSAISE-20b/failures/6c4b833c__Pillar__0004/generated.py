# -*- coding: utf-8 -*-
"""
Secure user role modification helper.
"""

from typing import Dict

# Example USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    # user_id: { "name": ..., "role": ... }
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int,
                     user_to_change_id: int,
                     new_privilege_level: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        The ID of the user attempting to change privileges.
    user_to_change_id : int
        The ID of the user whose privilege is being altered.
    new_privilege_level : str
        The new privilege level designated for that user.

    Returns
    -------
    bool
        True if the privilege modification is successful, otherwise False.
    """
    # Validate input types
    if not isinstance(modifying_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if not isinstance(new_privilege_level, str):
        return False

    # Normalise the new privilege level
    new_privilege_level = new_privilege_level.lower()

    # Ensure the requested role is valid
    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # Retrieve modifying user
    mod_user = USERS.get(modifying_user_id)
    if not mod_user:
        # Modifying user does not exist
        return False

    # Check that the modifying user has admin privileges
    if mod_user.get("role") != "admin":
        # Insufficient privileges to perform role change
        return False

    # Retrieve target user
    target_user = USERS.get(user_to_change_id)
    if not target_user:
        # Target user does not exist
        return False

    # Prevent privilege escalation to admin by non-admins (already checked)
    # Additional safety: disallow self‑promotion if not already admin
    if modifying_user_id == user_to_change_id and new_privilege_level != mod_user.get("role"):
        # User is attempting to change their own role
        if new_privilege_level != "admin":
            # Non‑admin cannot change their own role to anything else
            return False

    # Apply the role change
    target_user["role"] = new_privilege_level
    return True