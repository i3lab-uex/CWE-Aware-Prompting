# users data structure example (to be provided by the application)
USERS = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
    # ... other users
}

def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the role of a target user if the current user is an admin.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting the change.
    targ_user_id : int
        ID of the target user whose role is to be updated.
    privilege_change : str
        New role for the target user. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the role was updated successfully, False otherwise.
    """
    # Validate input types
    if not all(isinstance(arg, int) for arg in (curr_user_id, targ_user_id)):
        return False
    if not isinstance(privilege_change, str):
        return False

    # Define allowed roles
    ALLOWED_ROLES = {"normal", "moderator", "admin"}

    # Check that the privilege change is valid
    if privilege_change not in ALLOWED_ROLES:
        return False

    # Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None or targ_user is None:
        return False

    # Only admins can change roles
    if curr_user.get("role") != "admin":
        return False

    # Prevent downgrading an admin to a non-admin without explicit check
    if curr_user_id == targ_user_id:
        # Admin cannot change their own role to avoid accidental lockout
        return False

    # Perform the update
    try:
        targ_user["role"] = privilege_change
        return True
    except Exception:
        # In case USERS is not mutable or other unexpected errors occur
        return False