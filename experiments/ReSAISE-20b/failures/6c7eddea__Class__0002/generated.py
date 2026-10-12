# -*- coding: utf-8 -*-
"""
Utility module for managing user privileges.
"""

# Example USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice",   "role": "admin"},
#     2: {"name": "Bob",     "role": "moderator"},
#     3: {"name": "Charlie", "role": "normal"}
# }

USERS = {}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the administrator attempting to make the change.
    tar_user_id : int
        ID of the user whose privilege is being updated.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # Validate privilege update value
    allowed_privileges = {"normal", "moderator", "admin"}
    if priv_update not in allowed_privileges:
        return False

    # Check that both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Authorization check: only admins may change privileges
    if cur_user.get("role") != "admin":
        return False

    # Perform the update
    tar_user["role"] = priv_update
    return True


# ----------------- Example usage (for testing) -----------------
if __name__ == "__main__":
    # Populate sample USERS dictionary
    USERS.update(
        {
            1: {"name": "Alice", "role": "admin"},
            2: {"name": "Bob", "role": "moderator"},
            3: {"name": "Charlie", "role": "normal"},
        }
    )

    # Attempt to change Charlie's role to moderator by Alice
    success = alter_user_privileges(1, 3, "moderator")
    print("Success:", success)          # Expected: True
    print("Charlie's new role:", USERS[3]["role"])

    # Attempt unauthorized change by Bob
    success = alter_user_privileges(2, 3, "admin")
    print("Success:", success)          # Expected: False