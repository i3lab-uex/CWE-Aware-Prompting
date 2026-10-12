# -*- coding: utf-8 -*-

"""
This module provides a function for altering user privilege levels in a
system that manages users via the global USERS dictionary.

USERS is expected to be a dict of the form:
{
    user_id: {
        'role': str,          # e.g. 'normal', 'moderator', 'admin'
        'privilege': str,     # same values as role
    },
    ...
}
"""

from typing import Dict

# Example USERS dictionary. In real usage this would be imported or
# retrieved from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {'role': 'admin', 'privilege': 'admin'},
    2: {'role': 'moderator', 'privilege': 'moderator'},
    3: {'role': 'normal', 'privilege': 'normal'},
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int,
                          priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to modify privileges.
    tar_user_id : int
        ID of the target user whose privilege is to be updated.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Basic type checks (optional but helps guard against misuse)
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False
    if not isinstance(priv_update, str):
        return False

    # 1. Verify that the current user exists and is an admin
    cur_user = USERS.get(cur_user_id)
    if cur_user is None:
        return False
    if cur_user.get("privilege") != "admin":
        # Non-admins are not permitted to alter privileges
        return False

    # 2. Verify that the target user exists
    tar_user = USERS.get(tar_user_id)
    if tar_user is None:
        return False

    # 3. Validate the requested privilege level
    if priv_update not in VALID_PRIVILEGES:
        return False

    # 4. Prevent downgrading an admin to a lower privilege unless the target
    # is also an admin. This rule can be adjusted based on policy.
    if tar_user.get("privilege") == "admin" and priv_update != "admin":
        return False

    # 5. Apply the privilege change
    tar_user["privilege"] = priv_update
    return True


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    # Admin changing user 3 to moderator
    result = alter_user_privileges(1, 3, "moderator")
    print(f"Privilege change successful: {result}")   # Expected True