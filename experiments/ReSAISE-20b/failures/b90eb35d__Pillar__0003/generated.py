# -*- coding: utf-8 -*-
"""
Secure user privilege modification utility.

The function ensures that only users with the 'admin' role may modify
privileges of other accounts.  It validates the target user and the
requested privilege level before applying changes, preventing
improper access control (CWE‑284).
"""

from typing import Dict

# Example user store; in a real system this would be backed by
# persistent storage (e.g., database, LDAP).  Each entry maps a user_id
# to a dictionary containing at least the role and privilege level.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege":"moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege":"normal"},
    # ... more users
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the actor attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privileges are being modified.
    new_privilege : str
        The desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully modified, False otherwise.
    """
    # 1. Verify that the actor exists
    actor = USERS.get(current_user_id)
    if actor is None:
        return False

    # 2. Only admins may modify privileges
    if actor.get("role") != "admin":
        return False

    # 3. Verify that the target user exists
    target = USERS.get(target_user_id)
    if target is None:
        return False

    # 4. Validate the requested privilege
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 5. Prevent an admin from demoting themselves
    if current_user_id == target_user_id and new_privilege != "admin":
        return False

    # 6. Apply the change
    target["privilege"] = new_privilege
    return True