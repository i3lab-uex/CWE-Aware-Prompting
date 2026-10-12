from typing import Dict

# Example USERS dictionary structure:
# USERS = {
#     1: {"role": "admin", "privilege": "admin"},
#     2: {"role": "moderator", "privilege": "moderator"},
#     3: {"role": "user", "privilege": "normal"},
# }
USERS: Dict[int, dict] = {}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Alter the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the user attempting the change.
    tar_user_id : int
        ID of the target user whose privileges will be changed.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate privilege update value
    valid_privileges = {"normal", "moderator", "admin"}
    if priv_update not in valid_privileges:
        return False

    # Ensure both users exist
    cur_user = USERS.get(cur_user_id)
    tar_user = USERS.get(tar_user_id)
    if cur_user is None or tar_user is None:
        return False

    # Only an admin can modify privileges
    if cur_user.get("privilege") != "admin":
        return False

    # Prevent downgrading the administrator themselves
    if tar_user_id == cur_user_id and priv_update != "admin":
        return False

    # Perform the privilege change
    tar_user["privilege"] = priv_update
    return True