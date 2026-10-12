# change_user_role.py

from typing import Dict

# Sample USERS database structure
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "moderator"},
    3: {"name": "Charlie", "role": "normal"},
    # ... additional users
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
        The ID of the user whose privilege is being altered.
    new_privilege_level : str
        The new privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege modification was successful, False otherwise.
    """
    # 1. Validate new_privilege_level
    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # 2. Ensure both users exist
    if modifying_user_id not in USERS or user_to_change_id not in USERS:
        return False

    # 3. Authorization check: only admins can modify privileges
    if USERS[modifying_user_id]["role"] != "admin":
        return False

    # 4. Prevent admins from demoting themselves to a lower role
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False

    # 5. Apply the change
    USERS[user_to_change_id]["role"] = new_privilege_level
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Successful change
    assert change_user_role(1, 3, "moderator") is True
    # Unauthorized user tries to change role
    assert change_user_role(2, 3, "admin") is False
    # Invalid privilege level
    assert change_user_role(1, 3, "superuser") is False
    # Admin tries to demote themselves
    assert change_user_role(1, 1, "moderator") is False

    print("All tests passed.")