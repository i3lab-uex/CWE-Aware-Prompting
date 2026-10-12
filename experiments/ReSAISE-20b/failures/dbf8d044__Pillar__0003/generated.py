# -*- coding: utf-8 -*-
"""
Utility module to update user privilege levels with proper access control.

The function `update_user_privilege` ensures that only users with the
'admin' role may modify the privilege of other users.  It validates the
requested privilege level, checks that both actors exist in the USERS
dictionary and prevents users from changing their own privilege.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, Any

# Example USERS dictionary. In a real system this would be loaded from a
# secure data store or database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "bob",     "role": "moderator", "privilege": "moderator"},
    3: {"name": "charlie", "role": "normal",   "privilege": "normal"},
    4: {"name": "david",   "role": "admin",     "privilege": "admin"},
}

# Allowed privilege values
_ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the request.
    recipient_id : int
        ID of the target user whose privilege is to be changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    ValueError
        If any argument is invalid or if the actor lacks permission.
    """
    # Basic type checks
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        raise ValueError("actor_id and recipient_id must be integers")

    if not isinstance(updated_privilege, str):
        raise ValueError("updated_privilege must be a string")

    # Normalize privilege value
    updated_privilege = updated_privilege.lower()

    if updated_privilege not in _ALLOWED_PRIVILEGES:
        raise ValueError(f"Invalid privilege level: {updated_privilege}")

    # Ensure both users exist
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if actor is None or recipient is None:
        # One of the IDs does not exist
        return False

    # Prevent self-modification; admins can only change others
    if actor_id == recipient_id:
        return False

    # Only admins may modify privileges
    if actor.get("role") != "admin":
        return False

    # Perform the update
    recipient["privilege"] = updated_privilege
    return True


# Example usage (commented out; remove comments to test)
if __name__ == "__main__":
    print(update_user_privilege(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                     # Expected: "moderator"