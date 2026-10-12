# -*- coding: utf-8 -*-
"""
Module providing user role management functions.
"""

from typing import Dict

# Example USERS dictionary structure:
# USERS = {
#     1: {"role": "admin"},
#     2: {"role": "moderator"},
#     3: {"role": "normal"}
# }
USERS: Dict[int, Dict[str, str]] = {}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the change.
    targ_user_id : int
        ID of the user whose role is being modified.
    privilege_change : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the role was successfully updated, False otherwise.
    """
    # Basic input validation
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False

    if privilege_change not in VALID_PRIVILEGES:
        return False

    # Verify that both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None or targ_user is None:
        return False

    # Check that the requesting user has admin privileges
    if curr_user.get("role") != "admin":
        return False

    # Prevent a user from demoting themselves to lower privilege
    if curr_user_id == targ_user_id and privilege_change != "admin":
        return False

    # Perform the update
    try:
        targ_user["role"] = privilege_change
    except Exception:  # pragma: no cover
        return False

    return True