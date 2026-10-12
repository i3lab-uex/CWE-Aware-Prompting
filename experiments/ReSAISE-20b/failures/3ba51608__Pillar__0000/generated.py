# -*- coding: utf-8 -*-
"""
Utility to safely alter user privilege levels.

This module contains a single function `alter_user_permissions` that
verifies that the acting user has sufficient rights before changing a
target user's privilege level.  It protects against improper access control
(CWE-284) by ensuring only administrators can modify other users'
privileges.

Author: ChatGPT
"""

# Standard library imports
from typing import Dict

# Example USERS dictionary; in a real application this would be loaded from
# a database or secure configuration.  Each user record contains an `id`,
# `username`, and `role` field.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user, if and only if the acting user
    has administrator privileges.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    targeted_user_id : int
        ID of the user whose privilege level will be updated.
    new_privilege_level : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(acting_user_id, int) or not isinstance(targeted_user_id, int):
        return False
    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # Retrieve user records
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    # Both users must exist
    if acting_user is None or targeted_user is None:
        return False

    # Only admins may modify privileges
    if acting_user.get("role") != "admin":
        return False

    # Prevent self-demotion: an admin cannot lower their own privilege
    if acting_user_id == targeted_user_id and new_privilege_level != "admin":
        return False

    # Perform the update
    targeted_user["role"] = new_privilege_level
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful change
    assert alter_user_permissions(1, 3, "moderator") is True
    # Unauthorized user attempts change
    assert alter_user_permissions(2, 3, "admin") is False
    # Invalid privilege level
    assert alter_user_permissions(1, 3, "superuser") is False
    # Self-demotion attempt
    assert alter_user_permissions(1, 1, "normal") is False

    print("All tests passed.")