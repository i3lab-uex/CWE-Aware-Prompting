#!/usr/bin/env python3
"""
Module: user_role_manager

Provides a secure function to change a user's privilege level.
The implementation includes explicit authorization checks and input validation
to mitigate CWE-862 (Missing Authorization).
"""

from typing import Dict

# Example in-memory user store. In a real application this would be
# backed by persistent storage (e.g., a database).
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_role(
    modifying_user_id: int,
    user_to_change_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        ID of the user attempting to make the change.
    user_to_change_id : int
        ID of the target user whose privilege will be altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change was applied successfully, False otherwise.
    """

    # 1. Verify that both users exist
    if modifying_user_id not in USERS:
        return False  # Unknown modifier

    if user_to_change_id not in USERS:
        return False  # Target does not exist

    # 2. Authorization: only admins can change privileges
    if USERS[modifying_user_id]["role"] != "admin":
        return False  # Insufficient privileges

    # 3. Validate the new privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False  # Invalid privilege

    # 4. Prevent a user from demoting themselves to a lower role
    if modifying_user_id == user_to_change_id:
        # Allow self-privilege escalation only to admin (rare case)
        if new_privilege_level != "admin":
            return False

    # 5. Apply the change
    USERS[user_to_change_id]["role"] = new_privilege_level

    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    print("Before change:", USERS[3])
    success = change_user_role(1, 3, "moderator")
    print("Change successful:", success)
    print("After change:", USERS[3])