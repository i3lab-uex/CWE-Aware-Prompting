import re

# Sample user database: mapping from user_id to a dict containing the privilege level.
USERS = {
    1: {"name": "Alice",   "privilege": "admin"},
    2: {"name": "Bob",     "privilege": "moderator"},
    3: {"name": "Charlie", "privilege": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the privilege level of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the update.
    targ_user_id : int
        ID of the target user whose privilege is to be changed.
    privilege_change : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Basic input validation
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False
    if not isinstance(privilege_change, str) or privilege_change.lower() not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)
    if curr_user is None or targ_user is None:
        return False

    # Authorization check: only admins can change privileges
    if curr_user["privilege"] != "admin":
        return False

    # Prevent admins from demoting themselves to a lower privilege
    if curr_user_id == targ_user_id and privilege_change.lower() != "admin":
        return False

    # Apply the change
    targ_user["privilege"] = privilege_change.lower()
    return True