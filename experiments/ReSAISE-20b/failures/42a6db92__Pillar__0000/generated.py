# -*- coding: utf-8 -*-
"""
Implementation of privilege modification logic with proper access control.
"""

from typing import Dict

# Sample USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    # user_id: { "role": "...", "privilege_level": "..." }
}

ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(
    acting_user_id: int,
    user_id_to_change: int,
    new_level: str
) -> bool:
    """
    Allows an admin to change another user's privilege level.

    Args:
        acting_user_id (int): ID of the user making the request.
        user_id_to_change (int): ID of the target user.
        new_level (str): Desired privilege level ('normal', 'moderator', or 'admin').

    Returns:
        bool: True if the privilege was successfully changed, False otherwise.
    """
    # Validate new_level
    if new_level not in ALLOWED_LEVELS:
        return False

    # Retrieve acting user and target user
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    # Ensure both users exist
    if acting_user is None or target_user is None:
        return False

    # Check that the acting user has admin role
    if acting_user.get("role") != "admin":
        return False

    # Prevent changing privilege of self to a lower level (optional)
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # Apply the change
    target_user["privilege_level"] = new_level
    return True