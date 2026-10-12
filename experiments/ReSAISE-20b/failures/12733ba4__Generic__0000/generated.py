# USER_PROFILES maps user_id to a dictionary containing profile information.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

# USERS maps user_id to a dictionary containing user details including role.
USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}

def display_user_profile(active_user_id: int, profile_user_id: int):
    """
    Return the profile of `profile_user_id` if the active user has permission.
    
    Permission rules:
        - A user can view their own profile.
        - An admin (role == 'admin') can view any profile.
    
    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.
    
    Returns
    -------
    dict | str
        The profile dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    
    # Verify that both users exist in the system
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Admin check
    is_admin = USERS[active_user_id].get("role") == "admin"

    # Allow if same user or admin
    if active_user_id == profile_user_id or is_admin:
        return USER_PROFILES[profile_user_id]

    return "Unauthorized"