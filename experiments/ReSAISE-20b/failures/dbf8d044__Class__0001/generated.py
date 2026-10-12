# -*- coding: utf-8 -*-
"""
Utility to change user privilege levels in a simple in‑memory store.

The module deliberately performs minimal checks: it verifies that
* the actor exists and has a role of 'admin',
* the recipient exists,
* the requested privilege is one of the allowed values.

It does **not** persist changes to disk; it merely updates the global
`USERS` dictionary.
"""

from typing import Dict

# Example user store; in a real system this would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege": "normal"},
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        The ID of the user performing the request.
    recipient_id : int
        The ID of the user whose privilege is being changed.
    updated_privilege : str
        Desired privilege level: 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the change was applied, False otherwise.

    Raises
    ------
    KeyError
        If either the actor or recipient does not exist in USERS.
    ValueError
        If `updated_privilege` is not one of the allowed values.
    """
    # 1. Verify actor exists
    actor = USERS.get(actor_id)
    if actor is None:
        return False

    # 2. Authorization: only admins may change privileges
    if actor.get("role") != "admin":
        return False

    # 3. Verify recipient exists
    recipient = USERS.get(recipient_id)
    if recipient is None:
        return False

    # 4. Validate privilege value
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 5. Apply the change
    recipient["privilege"] = updated_privilege
    return True


# Example usage (for manual testing only)
if __name__ == "__main__":
    print(update_user_privilege(1, 2, "admin"))   # True
    print(USERS[2]["privilege"])                  # admin
    print(update_user_privilege(3, 1, "normal"))  # False (non-admin actor)
    print(update_user_privilege(1, 4, "normal"))  # False (recipient does not exist)