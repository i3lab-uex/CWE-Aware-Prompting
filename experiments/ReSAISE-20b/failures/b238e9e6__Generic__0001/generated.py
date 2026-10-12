import typing as _t

# Sample USERS dictionary for demonstration purposes.
# In a real application this would be persisted in a database or secure storage.
USERS: dict[int, dict[str, _t.Any]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(
    acting_user_id: int,
    affected_user_id: int,
    new_role: str
) -> bool:
    """
    Modify the role of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose role will be changed.
    new_role : str
        New privilege level for the affected user.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Raises
    ------
    KeyError
        If either user ID does not exist.
    ValueError
        If the new_role is invalid or the acting user lacks permission.
    """
    # Validate existence of both users
    if acting_user_id not in USERS:
        raise KeyError(f"Acting user ID {acting_user_id} does not exist.")
    if affected_user_id not in USERS:
        raise KeyError(f"Affected user ID {affected_user_id} does not exist.")

    # Validate new role
    if new_role not in ALLOWED_ROLES:
        raise ValueError(f"Invalid role '{new_role}'. Allowed roles: {ALLOWED_ROLES}")

    # Check permission: only admins can change privileges
    if USERS[acting_user_id]["role"] != "admin":
        return False

    # Prevent privilege escalation: an admin cannot demote themselves
    if acting_user_id == affected_user_id and new_role != "admin":
        return False

    # Perform the update
    USERS[affected_user_id]["role"] = new_role
    return True


# Example usage (uncomment to test)
# print(update_privileges(1, 3, "moderator"))  # Should return True
# print(USERS[3]["role"])  # Should be 'moderator'