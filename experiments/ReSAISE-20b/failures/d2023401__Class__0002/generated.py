# Change user privilege management module

# Example USERS dictionary structure:
# USERS = {
#     1: {"username": "alice", "role": "admin"},
#     2: {"username": "bob",   "role": "moderator"},
#     3: {"username": "carol", "role": "normal"}
# }

USERS = {}  # This should be populated by the application elsewhere


def change_user_privileges(active_user_id: int, affected_user_id: int, updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to make the change.
    affected_user_id : int
        The ID of the target user whose privileges are being modified.
    updated_privilege : str
        The new privilege level to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the operation succeeds, False otherwise.

    Notes
    -----
    - Only users with 'admin' role may modify other users.
    - The function checks that both user IDs exist and the target privilege is valid.
    - No external imports are required; the function operates purely on the USERS dict.
    """
    # Validate privilege level
    VALID_PRIVILEGES = {"normal", "moderator", "admin"}
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # Ensure both users exist
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if active_user is None or affected_user is None:
        return False

    # Authorization check: only admins can change privileges
    if active_user.get("role") != "admin":
        return False

    # Prevent an admin from demoting themselves to a lower role
    if active_user_id == affected_user_id and updated_privilege != "admin":
        return False

    # Apply the privilege change
    affected_user["role"] = updated_privilege
    return True