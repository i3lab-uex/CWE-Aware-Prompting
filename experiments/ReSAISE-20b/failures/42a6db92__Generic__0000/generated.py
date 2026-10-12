# users.py

USERS = {
    1: {"name": "Alice",   "role": "admin",     "privilege": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
    3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
    # Add more users as needed
}

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to modify the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    user_id_to_change : int
        The ID of the user whose privilege is being changed.
    new_level : str
        The desired privilege level for the target user. Must be one of
        'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege change was successful, False otherwise.
    """
    # Validate new_level
    valid_levels = {"normal", "moderator", "admin"}
    if new_level not in valid_levels:
        return False

    # Ensure acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Acting user must be an admin
    if acting_user.get("role") != "admin":
        return False

    # Ensure target user exists
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Prevent privilege escalation: admins cannot demote other admins
    if target_user.get("role") == "admin" and new_level != "admin":
        return False

    # Apply the change
    target_user["privilege"] = new_level

    return True