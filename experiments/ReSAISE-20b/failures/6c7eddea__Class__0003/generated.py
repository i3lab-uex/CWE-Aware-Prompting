# -*- coding: utf-8 -*-

"""
User privilege management module.

This module defines a function `alter_user_privileges` that allows an administrator
to change the privilege level of another user. The function performs rigorous
authorization checks to prevent unauthorized modifications and validates all
inputs before applying changes.

Author: ChatGPT
"""

from typing import Dict

# Example USERS dictionary structure.
# In a real system this would be fetched from a database or secure storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
    # Add more users as needed.
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to perform the change.
    tar_user_id : int
        ID of the target user whose privileges are to be modified.
    priv_update : str
        The new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False
    if priv_update not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Authorization check: only admins can change other users' privileges
    if cur_user_id == tar_user_id:
        # Users cannot modify their own privilege level
        return False

    if cur_user.get("role") != "admin":
        # Non-admin users are not allowed to alter privileges
        return False

    # Perform the privilege update
    tar_user["role"] = priv_update
    return True


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    print("Before:", USERS[3])
    success = alter_user_privileges(1, 3, "moderator")
    print("Success:", success)
    print("After:", USERS[3])