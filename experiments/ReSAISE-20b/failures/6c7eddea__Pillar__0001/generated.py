# -*- coding: utf-8 -*-

from typing import Dict

# Sample USERS dictionary structure:
# USERS = {
#     1: {"role": "admin"},
#     2: {"role": "moderator"},
#     3: {"role": "normal"}
# }
USERS: Dict[int, dict] = {}


def alter_user_privileges(cur_user_id: int,
                          tar_user_id: int,
                          priv_update: str) -> bool:
    """
    Allow an administrator to change the privilege level of another user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to perform the change.
    tar_user_id : int
        ID of the target user whose privileges will be updated.
    priv_update : str
        New privilege level to assign. Must be one of 'normal', 'moderator',
        or 'admin'.

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.

    Raises
    ------
    ValueError
        If priv_update is not a valid privilege level.
    """
    # Validate the new privilege value
    VALID_PRIVILEGES = {"normal", "moderator", "admin"}
    if priv_update not in VALID_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {priv_update}")

    # Check that the current user exists and has admin rights
    cur_user = USERS.get(cur_user_id)
    if not cur_user or cur_user.get("role") != "admin":
        return False

    # Ensure the target user exists
    tar_user = USERS.get(tar_user_id)
    if not tar_user:
        return False

    # Prevent self‑downgrading: an admin cannot reduce their own privileges
    if cur_user_id == tar_user_id and priv_update != "admin":
        return False

    # Perform the privilege update
    tar_user["role"] = priv_update
    return True