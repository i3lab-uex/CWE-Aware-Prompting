# -*- coding: utf-8 -*-

"""
User privilege management module.

The `update_privileges` function allows an administrator to change the role
of another user.  It enforces proper access control by verifying that
the acting user has the 'admin' role before making any changes.

CWE-284 (Improper Access Control) is mitigated by checking the
acting user's role and ensuring that only valid roles can be assigned.
"""

from typing import Dict

# Example user database.  In a real system this would be replaced by
# persistent storage (database, etc.).
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed roles
VALID_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user if the acting user is an administrator.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to change privileges.
    affected_user_id : int
        The ID of the user whose privilege is being altered.
    new_role : str
        The new privilege level to assign.

    Returns
    -------
    bool
        True if the role was successfully updated, False otherwise.
    """
    # Verify that both users exist
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None or affected_user is None:
        return False

    # Only admins can change roles
    if acting_user.get("role") != "admin":
        return False

    # Validate the new role
    if new_role not in VALID_ROLES:
        return False

    # Perform the update
    affected_user["role"] = new_role
    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(update_privileges(1, 3, "moderator"))  # Expected: True
#     print(USERS[3])                              # Expected role updated to "moderator"