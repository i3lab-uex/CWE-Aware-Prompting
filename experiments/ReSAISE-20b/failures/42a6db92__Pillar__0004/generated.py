import re

# Example USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice", "role": "admin", "privilege": "admin"},
#     2: {"name": "Bob",   "role": "moderator", "privilege": "moderator"},
#     3: {"name": "Carol", "role": "normal",    "privilege": "normal"},
# }
USERS = {}

def modify_privilege_level(acting_user_id: int, user_id_to_change: int, new_level: str) -> bool:
    """
    Allow an admin to change the privilege level of another user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the request.
    user_id_to_change : int
        ID of the target user whose privilege is to be changed.
    new_level : str
        Desired privilege level: 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.

    Notes
    -----
    - Only users with role 'admin' can modify privileges.
    - Admins cannot lower their own privilege level.
    - The target user must exist.
    - new_level is case‑insensitive but must match one of the allowed values.
    """
    # Validate input types
    if not all(isinstance(i, int) for i in (acting_user_id, user_id_to_change)):
        return False
    if not isinstance(new_level, str):
        return False

    # Normalise privilege string
    new_level = new_level.strip().lower()
    allowed_levels = {"normal", "moderator", "admin"}
    if new_level not in allowed_levels:
        return False

    # Fetch users
    acting_user = USERS.get(acting_user_id)
    target_user = USERS.get(user_id_to_change)

    # Check that both users exist
    if acting_user is None or target_user is None:
        return False

    # Check that the acting user has admin role
    if acting_user.get("role") != "admin":
        return False

    # Prevent admin from demoting themselves
    if acting_user_id == user_id_to_change and new_level != "admin":
        return False

    # All checks passed – perform the update
    target_user["privilege"] = new_level

    # Optionally keep role in sync with privilege
    if new_level == "admin":
        target_user["role"] = "admin"
    elif new_level == "moderator":
        target_user["role"] = "moderator"
    else:
        target_user["role"] = "normal"

    return True