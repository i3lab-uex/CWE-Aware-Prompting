# Sample data structures (replace with real data in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "eve",     "role": "user"},
}

def display_user_profile(active_user_id: int, profile_user_id: int):
    """
    Return the requested user profile if the active user is allowed to view it.
    
    Access rules:
        - A user can view their own profile.
        - An administrator (role == 'admin') can view any user's profile.
    
    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is granted, otherwise the string 'Unauthorized'.
    """
    # Validate that both user IDs exist in USERS
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the active user's role
    active_user_role = USERS[active_user_id].get("role", "")

    # Determine if access should be granted
    is_self = active_user_id == profile_user_id
    is_admin = active_user_role.lower() == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Return a copy to prevent accidental mutation of the global data
    return USER_PROFILES[profile_user_id].copy()