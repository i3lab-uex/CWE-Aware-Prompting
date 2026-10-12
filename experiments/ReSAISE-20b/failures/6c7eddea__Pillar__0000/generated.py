# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.

The `alter_user_privileges` function allows an administrator to change the
privilege level of another user.  It enforces strict access control by
requiring that the caller has `admin` privilege and that the requested
privilege level is one of the allowed values.

Author: OpenAI ChatGPT
"""

from typing import Dict

# Example USERS dictionary. In a real system this would be loaded from
# persistent storage or an external service.
USERS: Dict[int, str] = {
    1: 'admin',
    2: 'moderator',
    3: 'normal',
    # ... additional users ...
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {'normal', 'moderator', 'admin'}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting to perform the change.
    tar_user_id : int
        ID of the target user whose privileges are to be updated.
    priv_update : str
        Desired new privilege level for the target user.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate that both user IDs exist
    cur_priv = USERS.get(cur_user_id)
    tar_priv = USERS.get(tar_user_id)

    if cur_priv is None or tar_priv is None:
        # One of the users does not exist
        return False

    # Only admins may modify privileges
    if cur_priv != 'admin':
        return False

    # Validate requested privilege level
    if priv_update not in ALLOWED_PRIVILEGES:
        return False

    # Prevent a user from demoting themselves
    if cur_user_id == tar_user_id and priv_update != 'admin':
        return False

    # Perform the update
    USERS[tar_user_id] = priv_update
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    # Admin (ID 1) promotes user 3 to moderator
    print(alter_user_privileges(1, 3, 'moderator'))  # Expected: True
    print(USERS[3])                                 # Expected: 'moderator'

    # Non-admin attempts to demote user 2
    print(alter_user_privileges(2, 3, 'normal'))     # Expected: False
    print(USERS[3])                                 # Still 'moderator'