# -*- coding: utf-8 -*-
"""
Implementation of privilege modification with proper authorization checks.
"""

from typing import Dict

# Sample USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
    # Add more users as needed
}

# Allowed privilege levels
ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the request.
    user_id_to_change : int
        ID of the target user whose privilege level is to be changed.
    new_level : str
        Desired privilege level for the target user.

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Validate input types (basic defensive programming)
    if not isinstance(acting_user_id, int) or not isinstance(user_id_to_change, int):
        return False

    # Normalize the new level string
    new_level = new_level.strip().lower()
    if new_level not in ALLOWED_LEVELS:
        return False

    # Check that both users exist
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    if acting_user is None or target_user is None:
        return False

    # Authorization check: only admins may modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent an admin from demoting themselves (optional safety rule)
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # Perform the privilege level change
    target_user["role"] = new_level
    return True