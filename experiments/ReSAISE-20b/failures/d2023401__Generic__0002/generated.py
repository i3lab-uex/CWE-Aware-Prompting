# change_user_privileges.py

from typing import Dict, Any

# Example USERS dictionary; in a real system this would be loaded from a database or secure store
USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(active_user_id: int,
                           affected_user_id: int,
                           updated_privilege: str) -> bool:
    """
    Change the privilege level of a user in the USERS dictionary.

    Parameters
    ----------
    active_user_id : int
        ID of the user attempting the change. Must have role 'admin'.
    affected_user_id : int
        ID of the user whose privilege is to be updated.
    updated_privilege : str
        New privilege level. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege was updated successfully, False otherwise.
    """
    # Verify that both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if active_user is None or affected_user is None:
        # One of the users does not exist
        return False

    # Verify that the active user has admin privileges
    if active_user.get("role") != "admin":
        return False

    # Validate the requested privilege level
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Update the affected user's role
    try:
        affected_user["role"] = updated_privilege
        return True
    except Exception:
        # Catch unexpected errors (e.g., read‑only dict)
        return False