# -*- coding: utf-8 -*-
"""
Utility for modifying user privileges with proper access control.

The module defines a single function `alter_user_permissions` which
ensures that only users with the 'admin' privilege level can change the
privilege of any other user. It performs all necessary checks to avoid
CWE‑284 (Improper Access Control) vulnerabilities.

The `USERS` dictionary is expected to be defined in the same module
or imported from another module. Each user entry must contain a key
`'privilege'` with one of the values: 'normal', 'moderator', or
'admin'.
"""

from __future__ import annotations

# Example USERS dictionary; replace with the actual data source.
USERS: dict[int, dict[str, str]] = {
    1: {"username": "alice", "privilege": "admin"},
    2: {"username": "bob",   "privilege": "moderator"},
    3: {"username": "carol", "privilege": "normal"},
}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a target user if the acting user is an admin.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to modify privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate privilege levels
    valid_levels = {"normal", "moderator", "admin"}
    if new_privilege_level not in valid_levels:
        return False

    # Check existence of acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Verify that the acting user is an admin
    if acting_user.get("privilege") != "admin":
        return False

    # Check existence of targeted user
    target_user = USERS.get(targeted_user_id)
    if not target_user:
        return False

    # Prevent self-demotion to non-admin (optional safety check)
    if acting_user_id == targeted_user_id and new_privilege_level != "admin":
        return False

    # Perform the privilege update
    target_user["privilege"] = new_privilege_level
    return True


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(alter_user_permissions(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["privilege"])                     # Expected: 'moderator'