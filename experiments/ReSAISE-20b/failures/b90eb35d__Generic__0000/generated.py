from typing import Dict

# Example USERS dictionary structure:
USERS: Dict[int, Dict[str, str]] = {
    # user_id : {"username": str, "role": str, "privilege": str}
    1: {"username": "alice", "role": "admin",   "privilege": "admin"},
    2: {"username": "bob",   "role": "moderator","privilege": "moderator"},
    3: {"username": "carol", "role": "user",    "privilege": "normal"},
}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(current_user_id: int,
                           target_user_id: int,
                           new_privilege: str) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        ID of the actor attempting to modify privileges.
    target_user_id : int
        ID of the user whose privilege is being changed.
    new_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was changed, False otherwise.
    """
    # Verify that current user exists
    curr_user = USERS.get(current_user_id)
    if not curr_user:
        return False

    # Only admins can modify privileges
    if curr_user.get("privilege") != "admin":
        return False

    # Verify target user exists
    target_user = USERS.get(target_user_id)
    if not target_user:
        return False

    # Validate the new privilege value
    if new_privilege not in VALID_PRIVILEGES:
        return False

    # Update the privilege
    target_user["privilege"] = new_privilege
    return True