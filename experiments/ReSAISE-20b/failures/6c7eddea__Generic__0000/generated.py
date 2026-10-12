# -*- coding: utf-8 -*-
"""
Utility to modify user privileges in a simple in‑memory store.

The USERS dictionary is expected to be structured as:
{
    user_id: {
        "role": <str>,      # e.g., "normal", "moderator", "admin"
        ...
    },
    ...
}
"""

# Example USERS dictionary (replace with the real one in production)
USERS = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
}

# Accepted privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting the change.
    tar_user_id : int
        ID of the user whose privileges will be updated.
    priv_update : str
        New privilege level to assign ("normal", "moderator", or "admin").

    Returns
    -------
    bool
        True if the privilege was changed successfully, False otherwise.
    """
    # Validate privilege string
    if priv_update not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Only admins may change privileges
    if cur_user.get("role") != "admin":
        return False

    # Prevent downgrading the current admin to a non‑admin
    if cur_user_id == tar_user_id and priv_update != "admin":
        return False

    # Apply the update
    tar_user["role"] = priv_update
    return True


# Example usage (for testing only)
if __name__ == "__main__":
    print(alter_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                          # Expected: "moderator"