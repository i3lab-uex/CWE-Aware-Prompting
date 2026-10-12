# change_user_privileges.py

from typing import Dict

# Example USERS dictionary. In a real system this would be loaded from a database or secure store.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "privilege": "admin"},
    2: {"username": "bob",     "privilege": "moderator"},
    3: {"username": "charlie", "privilege": "normal"},
}

# Allowed privilege values
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(active_user_id: int, affected_user_id: int, updated_privilege: str) -> bool:
    """
    Allows an administrator to change the privilege level of another user.

    Args:
        active_user_id (int): ID of the user attempting to perform the change.
        affected_user_id (int): ID of the target user whose privilege will be updated.
        updated_privilege (str): New privilege level ('normal', 'moderator', or 'admin').

    Returns:
        bool: True if the privilege change was successful, False otherwise.
    """
    # Validate that both users exist
    if active_user_id not in USERS or affected_user_id not in USERS:
        return False

    # Authorization check: only admins may modify privileges
    if USERS[active_user_id]["privilege"] != "admin":
        return False

    # Prevent self-modification of admin privileges
    if active_user_id == affected_user_id and updated_privilege != USERS[active_user_id]["privilege"]:
        return False

    # Validate new privilege value
    if updated_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Perform the update
    USERS[affected_user_id]["privilege"] = updated_privilege
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(change_user_privileges(1, 2, "admin"))   # Expected: True
    print(USERS[2]["privilege"])                   # Expected: 'admin'