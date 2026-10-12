# Define user and profile data (example placeholders)
USERS = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "user"},
    3: {"name": "Charlie", "role": "user"},
}

USER_PROFILES = {
    1: {"email": "alice@example.com",   "age": 30},
    2: {"email": "bob@example.com",     "age": 25},
    3: {"email": "charlie@example.com", "age": 28},
}

def access_user_profile(active_user_id: int, profile_id: int):
    """
    Return the requested user's profile if the active user is authorized.

    An active user can view:
        * Their own profile (profile_id == active_user_id)
        * Any profile if they have the 'admin' role

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to view.

    Returns
    -------
    dict or str
        The requested profile data, or the string 'Unauthorized'.
    """
    # Validate that both users exist
    active_user = USERS.get(active_user_id)
    target_profile = USER_PROFILES.get(profile_id)

    if active_user is None or target_profile is None:
        return "Unauthorized"

    # Check authorization
    if active_user_id == profile_id or active_user.get("role") == "admin":
        return target_profile

    return "Unauthorized"