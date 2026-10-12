# -*- coding: utf-8 -*-
"""
User privilege management module.

This module defines a function `change_user_role` that allows an
administrator to modify the privilege level of another user.
The function enforces proper access control (CWE-284) by ensuring
only users with the 'admin' role can perform changes and that
the target privilege level is valid.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be
# replaced by persistent storage (e.g., database, external service).
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_role(
    modifying_user_id: int,
    user_to_change_id: int,
    new_privilege_level: str,
) -> bool:
    """
    Modify the privilege level of a user.

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
        True if the privilege modification succeeded, False otherwise.
    """
    # 1. Verify that both users exist
    if modifying_user_id not in USERS:
        return False  # Modifying user does not exist

    if user_to_change_id not in USERS:
        return False  # Target user does not exist

    # 2. Verify that the modifying user has admin privileges
    if USERS[modifying_user_id]["role"] != "admin":
        return False  # Not authorized

    # 3. Validate the requested privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False  # Invalid privilege level

    # 4. Optional: Prevent self-demotion (you may remove this if not desired)
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False  # Admin cannot demote themselves

    # 5. Perform the role change
    USERS[user_to_change_id]["role"] = new_privilege_level
    return True


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    # Admin Alice changes Bob to admin
    success = change_user_role(1, 2, "admin")
    print(f"Change succeeded: {success}")  # Expected: True

    # Bob (now admin) attempts to demote himself
    success = change_user_role(2, 2, "normal")
    print(f"Change succeeded: {success}")  # Expected: False (self-demotion prevented)