# -*- coding: utf-8 -*-

"""
User privilege management module.
"""

from typing import Dict

# Sample USERS dictionary structure:
# USERS = {
#     user_id: {"role": "normal" | "moderator" | "admin", ...}
# }
USERS: Dict[int, dict] = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
}

# Valid privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to make the modification.
    tar_user_id : int
        ID of the user whose privileges are being changed.
    priv_update : str
        New privilege level to assign to the target user.

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Basic validation: all IDs must be integers
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False

    # Ensure the privilege update is one of the allowed values
    if priv_update not in VALID_PRIVILEGES:
        return False

    # Verify that both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Only admins may alter privileges
    if cur_user.get("role") != "admin":
        return False

    # Prevent admins from demoting themselves to lower privilege
    if cur_user_id == tar_user_id and priv_update != "admin":
        return False

    # Perform the privilege update
    tar_user["role"] = priv_update
    return True


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Admin user 1 promotes user 3 to moderator
    result = alter_user_privileges(1, 3, "moderator")
    print(f"Privilege update successful: {result}")   # Expected: True
    print(USERS[3])  # Should show role 'moderator'