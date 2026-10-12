# -*- coding: utf-8 -*-
"""
Utility module for managing user privileges.
"""

from typing import Dict

# Example in-memory user store. In a real application this would be replaced
# with persistent storage (e.g., a database).
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",    "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"username": "charlie", "role": "user",     "privilege": "normal"},
    # ... additional users ...
}

# Allowed privilege values
_ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the operation.
    recipient_id : int
        ID of the user whose privilege is being changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully; False otherwise.
    """
    # Verify that both users exist
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if actor is None:
        # Actor does not exist
        return False

    if recipient is None:
        # Recipient does not exist
        return False

    # Only an admin can modify other users' privileges
    if actor.get("role") != "admin":
        return False

    # Validate the requested privilege level
    if updated_privilege not in _ALLOWED_PRIVILEGES:
        return False

    # Prevent privilege escalation or downgrades that could compromise security
    # e.g., a non-admin should not be able to grant 'admin' status.
    if updated_privilege == "admin" and actor.get("role") != "admin":
        return False

    # Perform the update
    recipient["privilege"] = updated_privilege
    return True