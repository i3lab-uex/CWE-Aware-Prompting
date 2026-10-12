# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.
"""

from typing import Dict

# Example structure of USERS dictionary:
# USERS = {
#     1: {"username": "alice",   "privilege": "admin"},
#     2: {"username": "bob",     "privilege": "moderator"},
#     3: {"username": "charlie", "privilege": "normal"}
# }
USERS: Dict[int, Dict[str, str]] = {}


def _is_valid_privilege(priv: str) -> bool:
    """Check if the privilege level is one of the allowed values."""
    return priv in {"normal", "moderator", "admin"}


def change_user_privileges(
    active_user_id: int,
    affected_user_id: int,
    updated_privilege: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    active_user_id : int
        ID of the user attempting to perform the change.
    affected_user_id : int
        ID of the user whose privileges are being updated.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """
    # Basic type checks
    if not all(isinstance(x, int) for x in (active_user_id, affected_user_id)):
        return False
    if not isinstance(updated_privilege, str):
        return False

    # Validate privilege string
    if not _is_valid_privilege(updated_privilege):
        return False

    # Ensure both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if active_user is None or affected_user is None:
        return False

    # Only admins can change privileges
    if active_user.get("privilege") != "admin":
        return False

    # Prevent changing privileges of self to a lower level
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Apply the change
    affected_user["privilege"] = updated_privilege
    return True