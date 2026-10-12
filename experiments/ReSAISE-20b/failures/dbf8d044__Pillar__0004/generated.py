# -*- coding: utf-8 -*-

"""
User privilege management module.

This module contains a single function, `update_user_privilege`, which
allows an administrative user to change the privilege level of another
user.  The implementation enforces proper access control and validates
inputs to mitigate CWE-284: Improper Access Control.
"""

from typing import Dict

# Example USERS dictionary.  In a real application this would be loaded
# from a database or another secure store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int,
                          updated_privilege: str) -> bool:
    """
    Update the privilege level of a user account.

    Parameters
    ----------
    actor_id : int
        The ID of the user making the request.
    recipient_id : int
        The ID of the user whose privilege is being changed.
    updated_privilege : str
        Desired privilege level for the target user. Must be one of
        ``'normal'``, ``'moderator'`` or ``'admin'``.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * The actor must exist and have the 'admin' role.
    * The recipient must exist in the USERS dictionary.
    * `updated_privilege` is validated against a whitelist of allowed
      values to prevent injection or accidental misuse.
    * The function performs no side‑effects other than updating the
      in‑memory USERS dict.  In a real system this would also persist
      changes to persistent storage.

    Security Considerations
    -----------------------
    This implementation protects against improper access control by
    enforcing that only users with the 'admin' role can change other
    users' privileges.  It also uses a strict whitelist for privilege
    values to avoid potential injection or misconfiguration attacks.
    """
    # Validate actor existence and role
    actor = USERS.get(actor_id)
    if not actor:
        # Actor does not exist
        return False

    if actor.get("role") != "admin":
        # Actor is not an admin
        return False

    # Validate recipient existence
    recipient = USERS.get(recipient_id)
    if not recipient:
        return False

    # Validate the requested privilege level
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # All checks passed – perform the update
    recipient["role"] = updated_privilege
    return True


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    print("Before:", USERS[3]["role"])
    success = update_user_privilege(actor_id=1, recipient_id=3,
                                    updated_privilege="moderator")
    print("Update succeeded:", success)
    print("After:", USERS[3]["role"])