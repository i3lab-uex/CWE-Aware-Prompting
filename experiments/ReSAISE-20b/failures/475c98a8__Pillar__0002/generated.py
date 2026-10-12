# -*- coding: utf-8 -*-

"""
User role management module.
"""

from typing import Dict

# Example user store. In a real system this would be replaced with a database.
USERS: Dict[int, str] = {
    1: "admin",
    2: "moderator",
    3: "normal",
    # Add more users as needed
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to change privileges.
    targ_user_id : int
        ID of the target user whose privilege is being changed.
    privilege_change : str
        New privilege level to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False

    if privilege_change not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    curr_role = USERS.get(curr_user_id)
    if curr_role is None:
        return False

    targ_role = USERS.get(targ_user_id)
    if targ_role is None:
        return False

    # Only an admin may change privileges
    if curr_role != "admin":
        return False

    # Optional: Prevent admins from demoting themselves or others to 'normal'
    # (uncomment if desired)
    # if curr_user_id == targ_user_id and privilege_change != "admin":
    #     return False

    # Apply the change
    USERS[targ_user_id] = privilege_change
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(update_user_roles(1, 3, "moderator"))  # Should return True
    print(USERS[3])  # Should now be 'moderator'