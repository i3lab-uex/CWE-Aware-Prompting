# modify_user_privileges.py

from typing import Dict

# Example USERS dictionary; in a real system this would be persisted elsewhere
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(current_user_id: int, target_user_id: int, new_privilege: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        ID of the user attempting the modification.
    target_user_id : int
        ID of the user whose privilege will be changed.
    new_privilege : str
        The new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully modified, otherwise False.
    """
    # Validate input types
    if not isinstance(current_user_id, int) or not isinstance(target_user_id, int):
        return False
    if new_privilege not in VALID_PRIVILEGES:
        return False

    # Check that both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        return False

    # Only admins may modify privileges
    if current_user.get("role") != "admin":
        return False

    # Prevent self‑promotion or demotion
    if current_user_id == target_user_id:
        return False

    # Apply the new privilege
    target_user["role"] = new_privilege
    return True