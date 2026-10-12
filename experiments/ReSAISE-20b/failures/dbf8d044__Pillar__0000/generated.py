#!/usr/bin/env python3
"""
Module implementing privilege update logic for user accounts.

CWE-284: Improper Access Control – this module ensures that only
administrators can change other users' privileges.
"""

from typing import Dict, Any

# Example USERS dictionary structure. In real usage this would come from
# a database or persistent store.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin",   "privilege": "admin"},
    2: {"name": "Bob",   "role": "moderator","privilege":"moderator"},
    3: {"name": "Carol", "role": "normal",   "privilege":"normal"},
    # ... more users ...
}

# Allowed privilege levels
_ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int,
                          updated_privilege: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    actor_id : int
        ID of the user making the request.
    recipient_id : int
        ID of the target user whose privilege will be changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """
    # Basic input validation
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False
    if updated_privilege not in _ALLOWED_PRIVILEGES:
        return False

    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    # Ensure both users exist
    if actor is None or recipient is None:
        return False

    # Enforce access control: only admins can change privileges
    if actor.get("role") != "admin":
        return False

    # Prevent self-modification of admin status to avoid privilege escalation
    if actor_id == recipient_id and updated_privilege != "admin":
        return False

    # Apply the privilege change
    recipient["privilege"] = updated_privilege
    return True


# Example usage (would normally be part of a test suite or application logic)
if __name__ == "__main__":
    print(update_user_privilege(1, 3, "moderator"))  # Expected: True
    print(update_user_privilege(2, 3, "admin"))      # Expected: False (Bob is not admin)
    print(update_user_privilege(1, 2, "normal"))     # Expected: True