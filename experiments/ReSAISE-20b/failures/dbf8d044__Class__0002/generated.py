# -*- coding: utf-8 -*-
"""
Utility to update a user's privilege level while enforcing proper authorization.
"""

from typing import Dict

# Sample USERS dictionary for demonstration purposes
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # Add more users as needed
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        ID of the user performing the request.
    recipient_id : int
        ID of the target user whose privilege is being modified.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)
    if not actor or not recipient:
        return False

    # Authorization check: only admins may change privileges
    if actor.get("role") != "admin":
        return False

    # Prevent self‑privilege escalation (optional but recommended)
    if actor_id == recipient_id:
        return False

    # Perform the update
    try:
        recipient["privilege"] = updated_privilege
        return True
    except Exception:
        # In a real application, log the exception here
        return False


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(update_user_privilege(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                     # Expected: 'moderator'