# -*- coding: utf-8 -*-

"""
A simple user privilege management module.
"""

from typing import Dict

# Sample USERS dictionary for demonstration purposes
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        The ID of the user attempting to make the change.
    tar_user_id : int
        The ID of the target user whose privilege will be updated.
    priv_update : str
        New privilege level to assign.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False

    if priv_update not in ALLOWED_PRIVILEGES:
        return False

    # Check that both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Authorization check: only admins may alter privileges
    if cur_user["privilege"] != "admin":
        return False

    # Prevent a user from demoting themselves to lower privilege
    if cur_user_id == tar_user_id and priv_update != "admin":
        return False

    # Perform the privilege update
    tar_user["privilege"] = priv_update
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Should succeed
    print(alter_user_privileges(1, 3, "moderator"))  # True
    # Should fail (non-admin attempting change)
    print(alter_user_privileges(2, 3, "admin"))      # False
    # Should fail (invalid privilege level)
    print(alter_user_privileges(1, 3, "superuser"))  # False