# -*- coding: utf-8 -*-

"""
Utility module for user privilege management.
"""

from typing import Dict

# Example USERS dictionary structure
# USERS = {
#     user_id: {"role": "normal" | "moderator" | "admin", ...}
# }
USERS: Dict[int, dict] = {}


def alter_user_privileges(cur_user_id: int,
                          tar_user_id: int,
                          priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to modify privileges.
    tar_user_id : int
        ID of the target user whose privilege is to be changed.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Validate privilege levels
    VALID_PRIVILEGES = {"normal", "moderator", "admin"}
    if priv_update not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Check that the current user has admin rights
    if cur_user.get("role") != "admin":
        return False

    # Prevent self‑promotion or demotion without admin rights
    if cur_user_id == tar_user_id:
        return False

    # Perform the update atomically
    try:
        tar_user["role"] = priv_update
        # In a real system you would persist the change to a database here.
    except Exception:
        return False

    return True