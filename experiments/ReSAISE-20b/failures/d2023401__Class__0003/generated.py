# -*- coding: utf-8 -*-

"""
User privilege management module.

This module provides a single public function, `change_user_privileges`, that
allows an administrator to modify the privilege level of another user in a
system.  The function performs proper authorization checks and input validation
to mitigate the risk of CWE-862: Missing Authorization.
"""

from typing import Dict

# Example user database.  In a real application this would be replaced by
# persistent storage (e.g., a database).  Each user record contains:
#   - `role`: a string indicating the user's current role.
#   - `privilege`: a string representing the privilege level.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
    # ... additional users ...
}

# Valid privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int,
    affected_user_id: int,
    updated_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to perform the change.
    affected_user_id : int
        The ID of the user whose privileges are to be updated.
    updated_privilege : str
        The new privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated; False otherwise.

    Raises
    ------
    ValueError
        If any of the input parameters are invalid.
    """
    # Validate that all user IDs exist
    if active_user_id not in USERS:
        return False  # Active user does not exist

    if affected_user_id not in USERS:
        return False  # Target user does not exist

    # Authorization check: only admins can change other users' privileges.
    active_user_role = USERS[active_user_id]["role"]
    if active_user_role != "admin":
        return False  # Not authorized

    # Prevent a user from demoting themselves to a lower privilege level
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Validate the requested privilege level
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Perform the update
    USERS[affected_user_id]["privilege"] = updated_privilege

    # In a real system, you would persist the change to a database here.

    return True