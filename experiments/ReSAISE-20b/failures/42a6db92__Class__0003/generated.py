# -*- coding: utf-8 -*-

from typing import Dict

# Sample USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice",   "role": "admin",    "privilege_level": "admin"},
#     2: {"name": "Bob",     "role": "moderator","privilege_level":"moderator"},
#     3: {"name": "Charlie", "role": "user",    "privilege_level":"normal"},
# }
USERS: Dict[int, dict] = {}

def modify_privilege_level(acting_user_id: int,
                           user_id_to_change: int,
                           new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user making the request.
    user_id_to_change : int
        ID of the target user whose privilege is being changed.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Validate input types early
    if not isinstance(acting_user_id, int) or not isinstance(user_id_to_change, int):
        return False
    if new_level not in {"normal", "moderator", "admin"}:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    if acting_user is None or target_user is None:
        return False

    # Authorization check: only admins may modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent privilege escalation on self (optional but safer)
    if acting_user_id == user_id_to_change:
        return False

    # Perform the update
    target_user["privilege_level"] = new_level

    # Optionally keep role in sync with privilege level
    target_user["role"] = new_level

    return True