# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.
"""

from typing import Dict

# Example in‑memory user store
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    targeted_user_id : int
        ID of the user whose privileges will be altered.
    new_privilege_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        ``True`` if the change succeeded, otherwise ``False``.

    Notes
    -----
    - Only users with an 'admin' role may modify privileges.
    - The targeted user must exist in ``USERS``.
    - ``new_privilege_level`` must be one of the allowed values.
    """
    # Validate acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False  # Acting user does not exist

    if acting_user.get("role") != "admin":
        return False  # Insufficient permissions

    # Validate targeted user
    target_user = USERS.get(targeted_user_id)
    if not target_user:
        return False  # Target user does not exist

    # Validate new privilege level
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False  # Invalid privilege level

    # Perform the update
    target_user["role"] = new_privilege_level
    return True


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(alter_user_permissions(1, 3, "moderator"))  # True
#     print(USERS[3])  # {'name': 'Charlie', 'role': 'moderator'}