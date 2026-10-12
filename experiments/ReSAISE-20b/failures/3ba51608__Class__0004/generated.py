# -*- coding: utf-8 -*-

# Sample USERS dictionary for demonstration purposes.
USERS = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(acting_user_id: int, targeted_user_id: int,
                            new_privilege_level: str) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    targeted_user_id : int
        ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if acting_user is None or targeted_user is None:
        return False

    # Authorization check: only admins can change privileges
    if acting_user.get("role") != "admin":
        return False

    # Perform the privilege change
    targeted_user["role"] = new_privilege_level
    return True