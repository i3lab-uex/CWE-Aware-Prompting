# -*- coding: utf-8 -*-
"""
Utility module for modifying user privileges.

The function ensures that only an administrator can change the privilege
level of another user.  It also prevents demoting a current admin to a lower
role and ensures that the target user exists.
"""

from typing import Dict

# Sample USERS dictionary. In a real application this would be loaded from
# a database or another persistent store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Define the allowed privilege levels in order of hierarchy.
PRIVILEGE_HIERARCHY = ["normal", "moderator", "admin"]


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        ID of the user performing the operation.
    target_user_id : int
        ID of the user whose privilege will be changed.
    new_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.

    Notes
    -----
    * Only users with the 'admin' role can modify privileges.
    * The function prevents demoting an existing admin to a lower privilege
      level.  This protects against accidental loss of administrative access.
    * If the target user does not exist or the requested privilege is invalid,
      the function returns False.
    """
    # Check that all involved users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        # Either actor or target does not exist
        return False

    # Authorization check: only admins may modify privileges
    if current_user.get("role") != "admin":
        return False

    # Validate the requested privilege
    if new_privilege not in PRIVILEGE_HIERARCHY:
        return False

    # Prevent demoting an existing admin to a lower role
    if target_user.get("role") == "admin" and new_privilege != "admin":
        return False

    # Apply the change
    target_user["role"] = new_privilege
    return True