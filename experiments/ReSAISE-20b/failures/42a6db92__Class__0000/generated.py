# -*- coding: utf-8 -*-

"""
Implementation of a privilege modification function with proper authorization checks.
"""

from typing import Dict

# Sample USERS dictionary for demonstration purposes
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(acting_user_id: int,
                           user_id_to_change: int,
                           new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the request.
    user_id_to_change : int
        ID of the target user whose privilege will be changed.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Basic type validation
    if not isinstance(acting_user_id, int) or not isinstance(user_id_to_change, int):
        return False

    # Verify acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Authorization: only admins may modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Verify target user exists
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Validate new privilege level
    if new_level not in ALLOWED_LEVELS:
        return False

    # Apply the change
    target_user["role"] = new_level
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    print(modify_privilege_level(1, 2, "admin"))  # True
    print(USERS[2]["role"])                      # admin