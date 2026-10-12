# -*- coding: utf-8 -*-
"""
Module providing a function to update user roles while enforcing proper authorization.
"""

from typing import Dict

# Example USERS dictionary. In a real system this would come from a database.
USERS: Dict[int, str] = {
    1: "admin",
    2: "moderator",
    3: "normal",
    # ... other users
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        The ID of the user attempting to perform the change.
    targ_user_id : int
        The ID of the target user whose privilege will be modified.
    privilege_change : str
        The new privilege level to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.

    Notes
    -----
    - The current user must have 'admin' privileges to modify any other user's role.
    - The target user must exist in the USERS dictionary.
    - The requested privilege level must be valid.
    """
    # Authorization check: ensure current user is an admin
    curr_role = USERS.get(curr_user_id)
    if curr_role != "admin":
        return False

    # Validate target user exists
    if targ_user_id not in USERS:
        return False

    # Validate privilege level
    if privilege_change not in VALID_PRIVILEGES:
        return False

    # Perform the update
    USERS[targ_user_id] = privilege_change
    return True