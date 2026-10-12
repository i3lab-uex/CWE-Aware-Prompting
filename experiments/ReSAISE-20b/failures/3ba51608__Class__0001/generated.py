#!/usr/bin/env python3
"""
Module: user_permissions

Provides a function to alter user privileges with proper authorization checks.
"""

from typing import Dict, Any

# Example USERS dictionary structure.
# In a real application this would be replaced with database access or similar.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    targeted_user_id : int
        ID of the user whose privilege will be changed.
    new_privilege_level : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Validate that the acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        # Acting user does not exist
        return False

    # Only an admin can change privileges
    if acting_user.get("role") != "admin":
        return False

    # Validate that the targeted user exists
    targeted_user = USERS.get(targeted_user_id)
    if not targeted_user:
        return False

    # Validate the new privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # Perform the privilege change
    targeted_user["role"] = new_privilege_level
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Admin Alice changes Bob to admin
    success = alter_user_permissions(1, 2, "admin")
    print(f"Privilege change successful: {success}")
    print(USERS[2])  # Should now show role 'admin'