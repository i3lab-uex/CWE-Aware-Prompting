# -*- coding: utf-8 -*-

"""
User role management module.

Provides a single function `change_user_role` that allows an administrator
to change the privilege level of another user.  The function includes
proper authorization checks to mitigate CWE‑862 (Missing Authorization).
"""

from typing import Dict

# Example in-memory user store.  In a real system this would be
# backed by a database or external service.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int,
                     user_to_change_id: int,
                     new_privilege_level: str) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        The ID of the user attempting to change privileges.
    user_to_change_id : int
        The ID of the target user whose privilege is to be changed.
    new_privilege_level : str
        The desired new role for the target user.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    * Only users with role 'admin' are allowed to perform this action.
    * The function validates that both user IDs exist and that the
      requested role is valid.
    """
    # Basic input validation
    if not isinstance(modifying_user_id, int) or not isinstance(user_to_change_id, int):
        return False

    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # Authorization check: only admins can change roles
    modifying_user = USERS.get(modifying_user_id)
    if not modifying_user:
        return False

    if modifying_user["role"] != "admin":
        # Not authorized
        return False

    # Ensure the target user exists
    target_user = USERS.get(user_to_change_id)
    if not target_user:
        return False

    # Prevent an admin from demoting themselves to a lower role
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False

    # Apply the role change
    target_user["role"] = new_privilege_level
    return True


# Example usage (commented out to keep the module importable)
if __name__ == "__main__":
    print("Before:", USERS[3])
    success = change_user_role(1, 3, "moderator")
    print("Success:", success)
    print("After :", USERS[3])