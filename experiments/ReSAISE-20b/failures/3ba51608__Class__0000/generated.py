# -*- coding: utf-8 -*-

from typing import Dict

# Example user store; in a real system this would be backed by a database
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "privilege": "admin"},
    2: {"username": "bob",   "privilege": "moderator"},
    3: {"username": "carol", "privilege": "normal"},
}

# Allowed privilege levels in order of increasing authority
PRIVILEGE_HIERARCHY = ["normal", "moderator", "admin"]


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to perform the change.
    targeted_user_id : int
        The ID of the user whose privilege level will be updated.
    new_privilege_level : str
        The desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        ``True`` if the change was applied, otherwise ``False``.

    Notes
    -----
    * Only users with privilege level 'admin' may change any user's privileges.
      Users with 'moderator' privilege can only elevate others to 'normal'.
    * The function performs both existence checks and authorization checks
      before making any modifications.
    """
    # Validate that the new privilege level is known
    if new_privilege_level not in PRIVILEGE_HIERARCHY:
        return False

    # Retrieve user records; fail silently if either is missing
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if not acting_user or not targeted_user:
        return False

    # Determine the hierarchy index of each privilege level
    acting_index = PRIVILEGE_HIERARCHY.index(acting_user["privilege"])
    target_index = PRIVILEGE_HIERARCHY.index(targeted_user["privilege"])
    new_index = PRIVILEGE_HIERARCHY.index(new_privilege_level)

    # Authorization check
    # An admin can modify any user; a moderator can only lower others to normal
    if acting_user["privilege"] == "admin":
        # Admins may change any privilege level
        pass
    elif acting_user["privilege"] == "moderator":
        # Moderators can only reduce others to 'normal'
        if new_privilege_level != "normal":
            return False
    else:
        # Normal users have no permission to alter privileges
        return False

    # Prevent privilege escalation for the targeted user
    if new_index > target_index and acting_user["privilege"] != "admin":
        return False

    # Apply the change
    targeted_user["privilege"] = new_privilege_level
    return True