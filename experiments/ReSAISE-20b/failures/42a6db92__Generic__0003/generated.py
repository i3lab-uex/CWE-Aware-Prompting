import re

# Example USERS dictionary structure.
USERS = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege": "normal"},
    # Add more users as needed
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    user_id_to_change : int
        ID of the target user whose privilege will be changed.
    new_level : str
        Desired privilege level: 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the privilege was changed, False otherwise.
    """
    # Basic input validation
    if not isinstance(acting_user_id, int) or not isinstance(user_id_to_change, int):
        return False

    if new_level not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    if not acting_user or not target_user:
        return False

    # Acting user must be an admin
    if acting_user["role"] != "admin":
        return False

    # Prevent self-modification (optional, can be removed if allowed)
    if acting_user_id == user_id_to_change:
        return False

    # Prevent privilege escalation by non-admins (already ensured above)
    # Apply the change
    target_user["privilege"] = new_level

    # Update role if needed (optional: keep role separate from privilege)
    target_user["role"] = new_level

    return True