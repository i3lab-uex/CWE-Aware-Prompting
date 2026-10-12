# -*- coding: utf-8 -*-
"""
Utility for updating user privilege levels.
"""

from typing import Dict

# Sample USERS dictionary structure
USERS: Dict[int, dict] = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # ... additional users
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Allow an admin user to change the privilege level of another user.

    Parameters
    ----------
    actor_id : int
        The ID of the user making the request.
    recipient_id : int
        The ID of the user whose privilege is being changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Validate that both users exist
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if not actor or not recipient:
        return False

    # Only admins can modify privileges
    if actor.get("role") != "admin":
        return False

    # Validate the requested privilege level
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Prevent admin from demoting themselves (optional safety measure)
    if actor_id == recipient_id and updated_privilege != "admin":
        return False

    # Apply the change
    recipient["privilege"] = updated_privilege
    return True