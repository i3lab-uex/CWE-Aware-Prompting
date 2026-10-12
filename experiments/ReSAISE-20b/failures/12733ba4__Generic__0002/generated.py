# Define sample data structures (replace with actual data in production)
USERS = {
    # user_id: { "role": "admin" | "user", ... }
}

USER_PROFILES = {
    # user_id: { profile data dict }
}


def display_user_profile(active_user_id: int, profile_user_id: int):
    """
    Return the requested user profile if the active user is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user making the request.
    profile_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary if access is allowed, otherwise the string
        'Unauthorized'.
    """
    # Verify that both users exist in our data stores
    if active_user_id not in USERS or profile_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the active user's role
    active_user = USERS.get(active_user_id, {})
    role = active_user.get("role", "user")

    # Access rules:
    # 1. Users can view their own profile.
    # 2. Admins can view any profile.
    if active_user_id == profile_user_id or role.lower() == "admin":
        return USER_PROFILES[profile_user_id]

    # If none of the conditions are met, deny access
    return "Unauthorized"