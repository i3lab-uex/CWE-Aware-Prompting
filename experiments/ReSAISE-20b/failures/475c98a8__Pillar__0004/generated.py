# -*- coding: utf-8 -*-

"""
User role management module.

The USERS dictionary is assumed to be pre‑populated elsewhere in the application.
Each key is a user id (int) and each value is a dictionary containing at least
the keys 'role' (str) and optionally other metadata.

Example USERS structure:
USERS = {
    1: {'role': 'admin', 'name': 'Alice'},
    2: {'role': 'moderator', 'name': 'Bob'},
    3: {'role': 'normal', 'name': 'Charlie'}
}
"""

from typing import Dict

# Example placeholder; in real code this would be imported from the application's
# data layer or configuration.
USERS: Dict[int, Dict[str, str]] = {}

ALLOWED_PRIVILEGES = {'normal', 'moderator', 'admin'}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the role of a target user if the current user is authorized.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the change.
    targ_user_id : int
        ID of the user whose role will be updated.
    privilege_change : str
        New role to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the role was updated successfully; False otherwise.

    Notes
    -----
    * Only users with the 'admin' role can modify other users' roles.
    * The function performs strict checks to avoid improper access control
      (CWE‑284). It verifies that both users exist, that the requested role is
      valid, and that the current user is indeed an administrator.
    * The function does not allow a user to demote themselves or change
      their own role, preventing accidental loss of privileges.
    """
    # Basic sanity checks: all IDs must be integers
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False

    # Retrieve user records
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    # Ensure both users exist
    if curr_user is None or targ_user is None:
        return False

    # Prevent self‑modification (optional but safer)
    if curr_user_id == targ_user_id:
        return False

    # Check that the current user has admin privileges
    if curr_user.get('role') != 'admin':
        return False

    # Validate the requested privilege level
    if privilege_change not in ALLOWED_PRIVILEGES:
        return False

    # Update the target user's role
    targ_user['role'] = privilege_change
    return True