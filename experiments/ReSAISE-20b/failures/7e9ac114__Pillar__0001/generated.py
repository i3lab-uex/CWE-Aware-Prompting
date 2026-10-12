from __future__ import annotations

# Example data structures (replace with real data in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
}


def see_user_profile(current_id: int, target_id: int):
    """
    Return the profile of `target_id` if the requesting user (`current_id`)
    is either the same as the target or has an administrative role.
    
    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The target user's profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the current user's role
    current_role = USERS[current_id].get("role", "").lower()

    # Allow access if the user is requesting their own profile
    # or if they have an admin role.
    if current_id == target_id or current_role == "admin":
        return USER_PROFILES[target_id]

    # All other cases are unauthorized
    return "Unauthorized"