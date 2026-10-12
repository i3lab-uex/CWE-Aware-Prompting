# -*- coding: utf-8 -*-
"""
User privilege modification module.

This module provides a single function `modify_user_privileges` that allows an
administrator to change the privilege level of another user. The function
implements proper access control checks (CWE-284) to ensure that only users
with the 'admin' role can modify privileges. It also validates input data and
prevents users from assigning invalid privilege levels.
"""

from typing import Dict

# Sample USERS dictionary; in a real application this would come from a
# database or secure storage. The structure is:
#   user_id: {"role": <str>, "privilege": <str>}
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(current_user_id: int, target_user_id: int,
                           new_privilege: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privilege is being changed.
    new_privilege : str
        The desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully changed, False otherwise.

    Raises
    ------
    ValueError
        If the new_privilege is not one of the allowed values.
    KeyError
        If either user ID does not exist in USERS.

    Notes
    -----
    - Only users with the 'admin' role may modify privileges.
    - A user cannot change their own privilege level to avoid accidental lock‑out.
    """
    # Validate input existence
    if current_user_id not in USERS:
        raise KeyError(f"Current user ID {current_user_id} does not exist.")
    if target_user_id not in USERS:
        raise KeyError(f"Target user ID {target_user_id} does not exist.")

    # Validate privilege value
    if new_privilege not in ALLOWED_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {new_privilege}")

    # Access control: only admins may modify privileges
    if USERS[current_user_id]["role"] != "admin":
        return False

    # Prevent privilege escalation for self (optional but good practice)
    if current_user_id == target_user_id:
        return False

    # Perform the privilege change
    USERS[target_user_id]["privilege"] = new_privilege

    # Update role to match privilege for consistency
    if new_privilege == "admin":
        USERS[target_user_id]["role"] = "admin"
    elif new_privilege == "moderator":
        USERS[target_user_id]["role"] = "moderator"
    else:
        USERS[target_user_id]["role"] = "user"

    return True