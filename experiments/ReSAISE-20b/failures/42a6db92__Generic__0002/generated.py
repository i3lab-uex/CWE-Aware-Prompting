# Users data structure – in a real system this would come from a database.
USERS = {
    1: {"name": "Alice",   "role": "admin",     "privilege_level": "admin"},
    2: {"name": "Bob",     "role": "moderator","privilege_level": "moderator"},
    3: {"name": "Charlie", "role": "user",     "privilege_level": "normal"},
    # ... more users ...
}

# Valid privilege levels
VALID_PRIVILEGE_LEVELS = {"normal", "moderator", "admin"}

def modify_privilege_level(acting_user_id: int,
                           user_id_to_change: int,
                           new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    user_id_to_change : int
        The ID of the target user whose privilege level is to be modified.
    new_level : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeds, False otherwise.
    """
    # Verify acting user exists and is an admin
    acting_user = USERS.get(acting_user_id)
    if not acting_user or acting_user["role"] != "admin":
        return False

    # Verify target user exists
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Validate new privilege level
    if new_level not in VALID_PRIVILEGE_LEVELS:
        return False

    # Prevent an admin from demoting themselves
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # Apply the change
    target_user["privilege_level"] = new_level
    return True