import re

# Example USERS dictionary structure:
# USERS = {
#     1: {"username": "alice", "privilege": "admin"},
#     2: {"username": "bob",   "privilege": "normal"},
#     ...
# }
USERS = {}

VALID_PRIVILEGES = {"normal", "moderator", "admin"}

def change_user_privileges(active_user_id: int, affected_user_id: int, updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        ID of the user attempting the change. Must have 'admin' privilege.
    affected_user_id : int
        ID of the target user whose privilege will be changed.
    updated_privilege : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully updated, False otherwise.
    """
    # Validate input types
    if not isinstance(active_user_id, int) or not isinstance(affected_user_id, int):
        return False
    if not isinstance(updated_privilege, str):
        return False

    # Normalise privilege string
    updated_privilege = updated_privilege.lower()

    # Ensure the new privilege is one of the allowed values
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Check that both users exist
    active_user = USERS.get(active_user_id)
    target_user = USERS.get(affected_user_id)

    if active_user is None or target_user is None:
        return False

    # Ensure the acting user has admin privileges
    if active_user.get("privilege") != "admin":
        return False

    # Prevent privilege escalation: an admin cannot demote another admin to a lower level
    if target_user.get("privilege") == "admin" and updated_privilege != "admin":
        # Optionally, allow admins to demote other admins if needed; here we disallow
        return False

    # Perform the update
    try:
        target_user["privilege"] = updated_privilege
        return True
    except Exception:
        # Catch unexpected errors (e.g., read-only dict)
        return False