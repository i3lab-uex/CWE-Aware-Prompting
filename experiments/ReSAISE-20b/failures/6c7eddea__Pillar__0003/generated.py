# -*- coding: utf-8 -*-
"""
Utility to change user privilege levels while enforcing proper access control.

The function ensures that only users with the 'admin' role may modify
another user's privileges. It validates input types, checks that the target
user exists, and confirms the requested privilege level is one of the
allowed values.

CWE-284 (Improper Access Control) mitigated by explicit role checks.
"""

from typing import Dict

# Example user store; in a real system this would be replaced by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
    # ... more users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to perform the change.
    tar_user_id : int
        ID of the target user whose privileges are to be updated.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Basic type checks to avoid accidental misuse
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False
    if not isinstance(priv_update, str):
        return False

    # Normalize privilege string
    priv_update = priv_update.strip().lower()
    if priv_update not in ALLOWED_PRIVILEGES:
        return False

    # Verify current user exists and has admin privileges
    cur_user = USERS.get(cur_user_id)
    if not cur_user or cur_user.get("privilege") != "admin":
        return False

    # Verify target user exists
    tar_user = USERS.get(tar_user_id)
    if not tar_user:
        return False

    # Prevent admin from demoting themselves to a lower privilege
    if cur_user_id == tar_user_id and priv_update != "admin":
        return False

    # Perform the update
    tar_user["privilege"] = priv_update
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(alter_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                     # Expected: "moderator"