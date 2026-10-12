from typing import Dict

# Example user store; in a real system this would be replaced with a database or secure storage
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice", "role": "admin", "privilege_level": "admin"},
    2: {"username": "bob",   "role": "moderator", "privilege_level": "moderator"},
    3: {"username": "carol", "role": "user",      "privilege_level": "normal"},
}

ALLOWED_LEVELS = {"normal", "moderator", "admin"}


def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allow an admin user to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    user_id_to_change : int
        The ID of the user whose privilege is being changed.
    new_level : str
        Desired privilege level for the target user ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was applied successfully, False otherwise.
    """
    # Validate acting user
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False
    if acting_user["role"] != "admin":
        # Only admins can change privileges
        return False

    # Validate target user
    target_user = USERS.get(user_id_to_change)
    if not target_user:
        return False

    # Validate new level
    if new_level not in ALLOWED_LEVELS:
        return False

    # Prevent an admin from demoting themselves
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # Apply change
    target_user["privilege_level"] = new_level
    return True