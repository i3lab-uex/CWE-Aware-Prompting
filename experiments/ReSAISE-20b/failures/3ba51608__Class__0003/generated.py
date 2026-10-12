# -*- coding: utf-8 -*-

"""
Module providing user privilege alteration functionality.
"""

from typing import Dict

# Example in-memory users database
USERS: Dict[int, dict] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Valid privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(acting_user_id: int, targeted_user_id: int,
                           new_privilege_level: str) -> bool:
    """
    Modify the privilege level of a target user if and only if the acting
    user has administrative rights.

    Args:
        acting_user_id (int): ID of the user attempting to change privileges.
        targeted_user_id (int): ID of the user whose privilege is being altered.
        new_privilege_level (str): Desired privilege level ('normal',
            'moderator', or 'admin').

    Returns:
        bool: True if the operation succeeded, False otherwise.
    """
    # Check that both users exist
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(targeted_user_id)

    if acting_user is None or target_user is None:
        # One of the users does not exist
        return False

    # Authorization check: only admins may alter privileges
    if acting_user.get("role") != "admin":
        return False

    # Validate the new privilege level
    if new_privilege_level not in VALID_PRIVILEGES:
        return False

    # Perform the update
    target_user["role"] = new_privilege_level
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(alter_user_permissions(1, 3, "moderator"))  # True
    print(USERS[3]["role"])                          # 'moderator'