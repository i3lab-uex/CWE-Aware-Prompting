# update_user_roles.py

from typing import Dict, Any

# Sample USERS dictionary structure:
# USERS = {
#     1: {"username": "alice", "role": "admin"},
#     2: {"username": "bob",   "role": "moderator"},
#     3: {"username": "carol", "role": "normal"}
# }
USERS: Dict[int, Dict[str, Any]] = {}

def update_user_roles(curr_user_id: int,
                      targ_user_id: int,
                      privilege_change: str) -> bool:
    """
    Update the role of a target user.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting the change.
    targ_user_id : int
        ID of the user whose role will be changed.
    privilege_change : str
        New role to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the role was updated successfully, False otherwise.
    """
    # Validate input types
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False
    if not isinstance(privilege_change, str):
        return False

    # Normalize privilege string
    privilege = privilege_change.strip().lower()
    allowed_privileges = {"normal", "moderator", "admin"}
    if privilege not in allowed_privileges:
        return False

    # Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None or targ_user is None:
        return False

    # Only admins may change roles
    if curr_user.get("role") != "admin":
        return False

    # Prevent demoting an admin to a lower role if the target is the only admin
    if targ_user.get("role") == "admin" and privilege != "admin":
        # Count current admins
        admin_count = sum(1 for u in USERS.values() if u.get("role") == "admin")
        # If this is the last admin, deny demotion
        if admin_count <= 1:
            return False

    # Perform the update
    targ_user["role"] = privilege
    return True