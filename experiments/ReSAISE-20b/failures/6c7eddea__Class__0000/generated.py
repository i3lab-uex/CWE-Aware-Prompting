# -*- coding: utf-8 -*-

"""
Implementation of the `alter_user_privileges` function.

The function performs a strict authorization check to ensure that only
users with an 'admin' privilege level can modify the privileges of other
user accounts. It validates that both the current user and target user
exist in the system, that the new privilege level is one of the allowed
values, and that a user cannot modify their own privileges.

The global `USERS` dictionary is expected to have the following
structure:

    USERS = {
        user_id: {
            'role': <str>,          # e.g. 'normal', 'moderator', 'admin'
            ...                      # other user fields
        },
        ...
    }

The function returns `True` if the privilege change is successful,
otherwise it returns `False`.
"""

from typing import Dict, Any

# Example USERS dictionary (this would normally be populated elsewhere)
USERS: Dict[int, Dict[str, Any]] = {
    1: {'role': 'admin', 'name': 'Alice'},
    2: {'role': 'moderator', 'name': 'Bob'},
    3: {'role': 'normal', 'name': 'Charlie'}
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {'normal', 'moderator', 'admin'}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user account.

    Parameters
    ----------
    cur_user_id : int
        The ID of the user attempting to perform the privilege change.
    tar_user_id : int
        The ID of the target user whose privileges are to be updated.
    priv_update : str
        The new privilege level to assign to the target user.

    Returns
    -------
    bool
        True if the privilege change was performed successfully,
        False otherwise.

    Notes
    -----
    - Only users with the 'admin' role may modify other users' privileges.
    - The target user must exist in the USERS dictionary.
    - The new privilege level must be one of ALLOWED_PRIVILEGES.
    - A user cannot modify their own privileges through this function
      (use a dedicated admin-only interface for self-modification if needed).
    """
    # Basic input validation
    if not isinstance(cur_user_id, int) or not isinstance(tar_user_id, int):
        return False
    if not isinstance(priv_update, str) or priv_update.lower() not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)

    if cur_user is None or tar_user is None:
        return False

    # Authorization check: only admins can modify others
    if cur_user.get('role') != 'admin':
        return False

    # Prevent a user from modifying their own privileges
    if cur_user_id == tar_user_id:
        return False

    # Apply the privilege change
    tar_user['role'] = priv_update.lower()
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    print(alter_user_privileges(1, 2, 'admin'))   # Should return True
    print(alter_user_privileges(2, 3, 'moderator'))  # Should return False (non-admin)
    print(alter_user_privileges(1, 4, 'normal'))   # Should return False (target does not exist)