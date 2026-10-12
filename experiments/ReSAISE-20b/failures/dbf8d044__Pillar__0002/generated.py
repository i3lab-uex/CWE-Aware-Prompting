# -*- coding: utf-8 -*-

"""
User privilege management module.

The function `update_user_privilege` allows an admin user to change the
privilege level of another user.  It performs strict access checks to
prevent CWE‑284 (Improper Access Control) vulnerabilities.
"""

from typing import Dict

# Sample USERS dictionary structure:
# {
#     1: {"name": "Alice", "role": "admin", "privilege": "admin"},
#     2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
#     3: {"name": "Carol", "role": "normal",    "privilege": "normal"},
# }
USERS: Dict[int, Dict[str, str]] = {}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int, updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        ID of the user making the request.
    recipient_id : int
        ID of the target user whose privilege is to be changed.
    updated_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """
    # --- Basic input validation -------------------------------------------------
    if not isinstance(actor_id, int) or not isinstance(recipient_id, int):
        return False
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # --- Retrieve actor and recipient -------------------------------------------
    actor = USERS.get(actor_id)
    recipient = USERS.get(recipient_id)

    if actor is None or recipient is None:
        # One of the users does not exist
        return False

    # --- Enforce access control -------------------------------------------------
    # Only admins can change privileges
    if actor.get("role") != "admin":
        return False

    # Prevent an admin from changing their own privilege
    if actor_id == recipient_id:
        return False

    # --- Apply the change -------------------------------------------------------
    try:
        recipient["privilege"] = updated_privilege
        # Optionally keep the role in sync with privilege for simplicity
        recipient["role"] = updated_privilege
    except Exception:
        # Any unforeseen error results in a failure signal
        return False

    return True


# -------------------------------------------------------------------------------
# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Setup sample users
    USERS.update(
        {
            1: {"name": "Alice", "role": "admin", "privilege": "admin"},
            2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
            3: {"name": "Carol", "role": "normal",    "privilege": "normal"},
        }
    )

    # Admin changing Bob's privilege
    print(update_user_privilege(1, 2, "admin"))   # Expected: True
    print(USERS[2])                              # Bob's new role/privilege

    # Non-admin attempting change
    print(update_user_privilege(2, 3, "moderator"))  # Expected: False