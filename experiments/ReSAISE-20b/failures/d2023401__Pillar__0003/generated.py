# -*- coding: utf-8 -*-

from typing import Dict

# Example user database structure:
# USERS = {
#     1: {"name": "Alice",   "role": "admin"},
#     2: {"name": "Bob",     "role": "moderator"},
#     3: {"name": "Charlie", "role": "normal"},
# }
USERS: Dict[int, dict] = {}

def change_user_privileges(active_user_id: int,
                           affected_user_id: int,
                           updated_privilege: str) -> bool:
    """
    Allows an administrator to change the privilege level of another user.

    Parameters
    ----------
    active_user_id : int
        ID of the user attempting to make the change.
    affected_user_id : int
        ID of the user whose privilege level is being updated.
    updated_privilege : str
        New privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully changed, False otherwise.
    """
    # Validate that both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if active_user is None or affected_user is None:
        return False

    # Only an admin can change privileges
    if active_user.get("role") != "admin":
        return False

    # Prevent privilege escalation by not allowing a user to grant themselves admin
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Ensure the new privilege is one of the allowed values
    if updated_privilege not in {"normal", "moderator", "admin"}:
        return False

    # Apply the change
    affected_user["role"] = updated_privilege
    return True