# -*- coding: utf-8 -*-

# Sample USERS dictionary. In a real application this would be loaded from a database.
USERS = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(current_user_id: int, target_user_id: int, new_privilege: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privilege level is to be changed.
    new_privilege : str
        The desired privilege level ("normal", "moderator", or "admin").

    Returns
    -------
    bool
        True if the privilege was successfully modified, False otherwise.
    """
    # Validate that both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        return False

    # Only admins can modify privileges
    if current_user.get("role") != "admin":
        return False

    # Validate new privilege
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Prevent downgrading an admin to a lower role unless the target is not an admin
    if target_user.get("role") == "admin" and new_privilege != "admin":
        # Optional: allow this only if the current user is a super-admin or other checks
        return False

    # Update privilege
    USERS[target_user_id]["role"] = new_privilege
    return True