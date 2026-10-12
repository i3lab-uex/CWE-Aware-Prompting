# -*- coding: utf-8 -*-
"""
Utility module to update user privileges.

The function performs a strict authorization check and validates
the new privilege value before applying the change.
"""

from typing import Dict

# Example USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator", "privilege": "moderator"},
    3: {"username": "charlie", "role": "normal",    "privilege": "normal"},
    # ... other users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a target user.

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
        True if the update succeeded, False otherwise.
    """
    # --- Basic existence checks -------------------------------------------------
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if not actor or not recipient:
        # Either the actor or recipient does not exist
        return False

    # --- Authorization check ----------------------------------------------------
    if actor["role"] != "admin":
        # Only admins are allowed to modify privileges
        return False

    # Optional: prevent self‑privilege escalation (if desired)
    if actor_id == recipient_id:
        # Admins cannot change their own privilege level
        return False

    # --- Validate new privilege --------------------------------------------------
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # --- Apply the change --------------------------------------------------------
    recipient["privilege"] = updated_privilege
    return True


# --------------------------------------------------------------------
# Example usage (uncomment to test)
#
# if __name__ == "__main__":
#     print(update_user_privilege(1, 2, "admin"))   # True
#     print(USERS[2]["privilege"])                  # admin
#     print(update_user_privilege(2, 3, "admin"))   # False (non‑admin actor)
# --------------------------------------------------------------------