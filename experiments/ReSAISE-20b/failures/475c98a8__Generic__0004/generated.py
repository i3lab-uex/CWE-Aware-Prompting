# users.py (example USERS dictionary)
USERS = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the role of a target user if the current user has admin privileges.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting the modification.
    targ_user_id : int
        ID of the target user whose role is to be changed.
    privilege_change : str
        New role to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the role was updated successfully, False otherwise.
    """
    # Allowed roles
    ALLOWED_ROLES = {"normal", "moderator", "admin"}

    # Basic validation
    if privilege_change not in ALLOWED_ROLES:
        return False

    # Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None or targ_user is None:
        return False

    # Only admins can change roles
    if curr_user["role"] != "admin":
        return False

    # Prevent downgrading the admin that is making the change (optional safety)
    if curr_user_id == targ_user_id and privilege_change != "admin":
        return False

    # Apply the change
    targ_user["role"] = privilege_change
    return True


# Example usage:
if __name__ == "__main__":
    print(update_user_roles(1, 3, "moderator"))  # True
    print(USERS[3]["role"])                      # 'moderator'