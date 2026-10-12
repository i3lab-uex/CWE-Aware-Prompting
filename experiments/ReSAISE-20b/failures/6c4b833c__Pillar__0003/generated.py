import re

# Example USERS dictionary (replace with actual data source)
USERS = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_role(modifying_user_id: int, user_to_change_id: int, new_privilege_level: str) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        The ID of the user attempting to make the change.
    user_to_change_id : int
        The ID of the target user whose privilege is to be changed.
    new_privilege_level : str
        The desired new privilege level.

    Returns
    -------
    bool
        True if the change was successful, False otherwise.
    """
    # Basic input validation
    if not isinstance(modifying_user_id, int) or not isinstance(user_to_change_id, int):
        return False

    if new_privilege_level not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    if modifying_user_id not in USERS or user_to_change_id not in USERS:
        return False

    # Prevent privilege escalation: only admins can change privileges
    if USERS[modifying_user_id]["role"] != "admin":
        return False

    # Prevent a user from changing their own role to admin (optional security measure)
    if modifying_user_id == user_to_change_id and new_privilege_level == "admin":
        return False

    # Perform the role change
    USERS[user_to_change_id]["role"] = new_privilege_level
    return True