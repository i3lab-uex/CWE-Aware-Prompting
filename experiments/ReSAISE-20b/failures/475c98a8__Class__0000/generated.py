#!/usr/bin/env python3
"""
Module: user_role_manager

Provides a single function `update_user_roles` that safely updates the
privilege level of a target user, ensuring only administrators can perform
the change and that all inputs are validated.

The function assumes a global dictionary `USERS` exists with the
following structure:

    USERS = {
        1: {"name": "alice",   "role": "admin"},
        2: {"name": "bob",     "role": "moderator"},
        3: {"name": "charlie", "role": "normal"},
        ...
    }

Only the `"role"` key is relevant for authorization checks.
"""

from typing import Dict

# Example USERS dictionary (for illustration; replace with actual data source)
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "alice",   "role": "admin"},
    2: {"name": "bob",     "role": "moderator"},
    3: {"name": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int,
                      privilege_change: str) -> bool:
    """
    Update the role of `targ_user_id` to `privilege_change`.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the update.
    targ_user_id : int
        ID of the target user whose role will be changed.
    privilege_change : str
        New role to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * Only users with role 'admin' may modify other users.
    * The function does not allow a user to change their own role.
    * Input validation ensures that the target exists and the new role is
      valid.  If any check fails, False is returned.
    """
    # --- Authorization: ensure current user exists and is an admin ---
    curr_user = USERS.get(curr_user_id)
    if not curr_user:
        # Current user does not exist
        return False

    if curr_user.get("role") != "admin":
        # Current user is not authorized
        return False

    # --- Prevent self-modification ---
    if curr_user_id == targ_user_id:
        return False

    # --- Validate target user existence ---
    target_user = USERS.get(targ_user_id)
    if not target_user:
        return False

    # --- Validate new privilege level ---
    if privilege_change not in ALLOWED_PRIVILEGES:
        return False

    # --- Perform the update ---
    target_user["role"] = privilege_change
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful update
    print(update_user_roles(1, 2, "admin"))   # Expected: True

    # Attempt by non-admin
    print(update_user_roles(2, 3, "moderator"))  # Expected: False

    # Invalid privilege
    print(update_user_roles(1, 3, "superuser"))  # Expected: False

    # Self-modification attempt
    print(update_user_roles(1, 1, "normal"))     # Expected: False

    # Target user does not exist
    print(update_user_roles(1, 999, "normal"))   # Expected: False