# Constants representing user data and profiles
USERS = {
    # Example structure: {user_id: {"role": "admin" or "user", ...}}
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

USER_PROFILES = {
    # Example structure: {user_id: profile_data}
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}


def display_user_profile(active_user_id: int, profile_user_id: int):
    """
    Return the requested user profile if the active user is allowed to view it.
    An admin can view any profile; a regular user can only view their own.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the active user's role
    active_user_role = USERS.get(active_user_id, {}).get("role", "user")

    # Authorization logic
    if active_user_role == "admin" or active_user_id == profile_user_id:
        return USER_PROFILES.get(profile_user_id)

    # Deny access
    return "Unauthorized"