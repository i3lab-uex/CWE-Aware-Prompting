# -*- coding: utf-8 -*-
"""
Implementation of an access‑controlled user privilege change function.

The module protects against CWE‑284 (Improper Access Control) by enforcing
that only users with the 'admin' privilege may modify other users' roles,
and that the new privilege is one of the allowed values.
"""

from typing import Dict

# Example USERS dictionary structure.
# In a real application this would be replaced by a database or secure store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
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
        The ID of the user attempting to perform the change.
    user_to_change_id : int
        The ID of the target user whose role will be updated.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the role was successfully updated, False otherwise.
    """
    # Validate that both users exist
    if modifying_user_id not in USERS:
        return False
    if user_to_change_id not in USERS:
        return False

    # Verify that the modifying user has admin privileges
    if USERS[modifying_user_id]["role"] != "admin":
        return False

    # Validate the new privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # Prevent an admin from demoting themselves to a lower privilege
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False

    # Perform the role change
    USERS[user_to_change_id]["role"] = new_privilege_level
    return True


# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(change_user_role(1, 2, "admin"))   # True
#     print(USERS[2]["role"])                   # admin