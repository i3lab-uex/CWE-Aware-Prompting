# -*- coding: utf-8 -*-
"""
User privilege management module.

This module defines a simple in‑memory user store and provides the
`update_user_privilege` function which allows an admin user to modify
the privilege level of another user.

The users are represented by a global dictionary `USERS`.  Each entry
maps an integer user ID to a dictionary containing at least the keys:
    - 'role':      str   ("admin", "moderator" or "normal")
    - 'privilege': str   same values as role
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Example user store (in a real application this would be backed by a DB)
# --------------------------------------------------------------------------- #
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin",      "privilege": "admin"},
    2: {"role": "moderator",  "privilege": "moderator"},
    3: {"role": "normal",     "privilege": "normal"},
}

# --------------------------------------------------------------------------- #
# Helper constants
# --------------------------------------------------------------------------- #
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_privilege(actor_id: int, recipient_id: int,
                          updated_privilege: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    actor_id : int
        ID of the user making the request.
    recipient_id : int
        ID of the target user whose privilege is to be changed.
    updated_privilege : str
        Desired privilege level for the target user. Must be one of
        'normal', 'moderator' or 'admin'.

    Returns
    -------
    bool
        True if the privilege change was applied successfully,
        False otherwise.

    Notes
    -----
    * Only users with the 'admin' role are permitted to change other
      users' privileges.
    * The function does not allow a user to change their own privilege
      level.  This prevents accidental lock‑outs.
    * The function validates that the target user exists and that
      the requested privilege is valid.
    """
    # Validate that actor exists
    actor = USERS.get(actor_id)
    if not actor:
        return False

    # Actor must be an admin
    if actor.get("role") != "admin":
        return False

    # Prevent self‑privilege modification
    if actor_id == recipient_id:
        return False

    # Validate target user exists
    recipient = USERS.get(recipient_id)
    if not recipient:
        return False

    # Validate privilege value
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Apply the change
    recipient["privilege"] = updated_privilege
    return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print("Before:", USERS[3]["privilege"])
    success = update_user_privilege(1, 3, "moderator")
    print("Success:", success)
    print("After :", USERS[3]["privilege"])