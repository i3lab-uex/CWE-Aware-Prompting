import re

# Sample USERS dictionary structure:
# USERS = {
#     1: {"name": "Alice",   "role": "admin",    "privilege": "admin"},
#     2: {"name": "Bob",     "role": "moderator","privilege": "moderator"},
#     3: {"name": "Charlie", "role": "normal",   "privilege": "normal"},
# }
USERS = {}

def _validate_privilege(level: str) -> bool:
    """Check if the privilege level is one of the allowed values."""
    return level in {"normal", "moderator", "admin"}

def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Allow an admin user to change the privilege level of another user.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is to be changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was updated, False otherwise.
    """
    # Basic type checks to guard against injection or accidental misuse
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False
    if not isinstance(desired_privilege, str) or not _validate_privilege(desired_privilege):
        return False

    # Ensure both users exist
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # Only admins can modify privileges
    if requester.get("role") != "admin":
        return False

    # Prevent privilege escalation: an admin cannot demote themselves to non-admin
    if requesting_user_id == user_to_change_id and desired_privilege != "admin":
        return False

    # Apply the change
    target["privilege"] = desired_privilege
    return True