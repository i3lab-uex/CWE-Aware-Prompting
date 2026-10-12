# change_user_role.py

from typing import Dict, Any

# Sample user database (in a real application this would be persistent storage)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "moderator"},
    3: {"name": "Carol", "role": "normal"},
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
        ID of the user attempting to perform the change.
    user_to_change_id : int
        ID of the target user whose role is to be updated.
    new_privilege_level : str
        Desired new privilege level.

    Returns
    -------
    bool
        True if the role change succeeded, False otherwise.
    """
    # 1. Validate that both users exist
    mod_user = USERS.get(modifying_user_id)
    target_user = USERS.get(user_to_change_id)

    if mod_user is None or target_user is None:
        return False

    # 2. Authorization check – only admins can change roles
    if mod_user.get("role") != "admin":
        return False

    # 3. Validate new privilege level
    if new_privilege_level not in ALLOWED_ROLES:
        return False

    # 4. Prevent a user from demoting themselves to avoid lock‑out
    if modifying_user_id == user_to_change_id and new_privilege_level != "admin":
        return False

    # 5. Perform the update
    target_user["role"] = new_privilege_level
    return True


# Example usage (for demonstration purposes only)
if __name__ == "__main__":
    # Admin Alice changes Bob's role to admin
    result = change_user_role(1, 2, "admin")
    print(f"Role change successful: {result}")   # Expected: True

    # Non‑admin Bob tries to demote Carol
    result = change_user_role(2, 3, "normal")
    print(f"Role change successful: {result}")   # Expected: False