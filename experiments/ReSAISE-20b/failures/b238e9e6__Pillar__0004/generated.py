# -*- coding: utf-8 -*-
"""
User privilege management module.

This module provides a single function, `update_privileges`, which
allows an administrator to change the role of another user.
"""

from typing import Dict

# Example USERS dictionary; in a real application this would be loaded
# from persistent storage (e.g., database) rather than hard‑coded.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
    # Add more users as needed
}

# Allowed roles for validation purposes.
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Update the role of a user in the USERS dictionary.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to change privileges.
    affected_user_id : int
        The ID of the user whose privilege is being altered.
    new_role : str
        The new privilege level designated for that user.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * Only users with role 'admin' are permitted to change other users'
      roles.
    * The new_role must be one of the values in ALLOWED_ROLES.
    * If either user ID does not exist, the function returns False.

    Security
    --------
    This implementation prevents improper access control (CWE‑284) by
    ensuring that only administrators can perform privilege changes.
    """
    # Validate existence of acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Verify that the acting user is an administrator
    if acting_user.get("role") != "admin":
        return False

    # Validate existence of affected user
    if affected_user_id not in USERS:
        return False

    # Validate new role
    if new_role not in ALLOWED_ROLES:
        return False

    # Perform the update
    USERS[affected_user_id]["role"] = new_role
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Should succeed: admin changing Bob's role to 'admin'
    print(update_privileges(1, 2, "admin"))   # Expected: True

    # Should fail: Bob (moderator) attempting to demote Charlie
    print(update_privileges(2, 3, "normal"))  # Expected: False

    # Verify change
    print(USERS[2]["role"])  # Expected: 'admin'