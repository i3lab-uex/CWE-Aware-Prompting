from typing import Dict, Any

# Example USERS dictionary structure.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin", "privilege": "admin"},
    2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
    3: {"name": "Carol", "role": "normal",   "privilege": "normal"},
    # Add more users as needed.
}

ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user making the request.
    user_id_to_change : int
        ID of the target user whose privilege will be modified.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was applied successfully, False otherwise.
    """
    # Verify acting user exists and is an admin
    acting_user = USERS.get(acting_user_id)
    if not acting_user or acting_user.get("role") != "admin":
        return False

    # Verify target user exists
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Validate new privilege level
    if new_level not in ALLOWED_PRIVILEGES:
        return False

    # Prevent lowering an admin's own privilege
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # Apply the change
    target_user["privilege"] = new_level
    return True

# Example usage (uncomment to test)
# print(modify_privilege_level(1, 2, "admin"))  # Should return True
# print(USERS[2]["privilege"])                  # Should now be 'admin'