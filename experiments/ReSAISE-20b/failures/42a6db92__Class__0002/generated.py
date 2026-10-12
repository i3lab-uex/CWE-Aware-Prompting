# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.
"""

from typing import Dict

# Example USERS dictionary structure. In a real application this would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege_level": "admin"},
    2: {"username": "bob",     "role": "moderator", "privilege_level": "moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege_level": "normal"},
    # ... more users ...
}

# Allowed privilege levels
ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    user_id_to_change : int
        The ID of the target user whose privilege is to be changed.
    new_level : str
        Desired privilege level for the target user. Must be one of 'normal',
        'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.

    Notes
    -----
    - Authorization check: only users with role 'admin' can perform the change.
    - Validation of `new_level` ensures only known privilege levels are accepted.
    - The function does not raise exceptions for invalid input; it simply returns False.
    """
    # Validate existence of acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist
        return False

    # Authorization check: only admins can modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Validate existence of target user
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        # Target user does not exist
        return False

    # Validate new privilege level
    if new_level not in ALLOWED_LEVELS:
        return False

    # Apply the change
    target_user["privilege_level"] = new_level
    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Should succeed: admin changes Bob's level to normal
    print(modify_privilege_level(1, 2, "normal"))  # Expected: True

    # Should fail: non-admin user attempts change
    print(modify_privilege_level(2, 3, "moderator"))  # Expected: False

    # Should fail: invalid privilege level
    print(modify_privilege_level(1, 3, "superadmin"))  # Expected: False