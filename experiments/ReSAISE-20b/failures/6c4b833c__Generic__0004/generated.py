#!/usr/bin/env python3
"""
Utility module for user privilege management.

The module defines a global USERS dictionary that stores user data.
Each user entry is itself a dictionary containing at least the keys:
    - 'id': int
    - 'role': str  (one of 'normal', 'moderator', 'admin')
"""

from typing import Dict

# Sample in-memory user store. In a real application this would be
# backed by a database or persistent storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"id": 1, "role": "admin"},
    2: {"id": 2, "role": "moderator"},
    3: {"id": 3, "role": "normal"},
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
        The ID of the user attempting to make the change.
    user_to_change_id : int
        The ID of the target user whose role is to be updated.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the role change was successful, False otherwise.

    Notes
    -----
    - Only users with an 'admin' role may modify other users.
    - The function performs basic validation and does not persist changes
      beyond the in-memory USERS dictionary.
    - The function is intentionally simple; production code should use
      proper authentication, logging, and database transactions.
    """
    # Validate that the new privilege level is known
    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # Fetch modifying user
    modifier = USERS.get(modifying_user_id)
    if not modifier:
        # Modifying user does not exist
        return False

    # Only admins can change roles
    if modifier["role"] != "admin":
        return False

    # Fetch target user
    target = USERS.get(user_to_change_id)
    if not target:
        # Target user does not exist
        return False

    # Prevent self-demotion of an admin (optional safeguard)
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False

    # Apply the role change
    target["role"] = new_privilege_level
    return True


# Example usage (for demonstration only; remove or guard with __name__ == "__main__" in real code)
if __name__ == "__main__":
    print(change_user_role(1, 2, "admin"))   # True
    print(USERS[2]["role"])                  # 'admin'