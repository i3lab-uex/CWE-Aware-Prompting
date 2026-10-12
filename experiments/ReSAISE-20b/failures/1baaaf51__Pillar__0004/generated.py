from typing import Dict, Any

# Sample data structures (these would normally be loaded from a database or other storage)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Administrator"},
    2: {"email": "bob@example.com",   "bio": "Regular user"},
    3: {"email": "carol@example.com", "bio": "Another user"},
}


def access_user_profile(active_user_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if access is permitted, otherwise return 'Unauthorized'.

    Parameters
    ----------
    active_user_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile to view.

    Returns
    -------
    dict or str
        The requested profile dictionary, or the string 'Unauthorized'.
    """
    # Verify that both users exist
    active_user = USERS.get(active_user_id)
    requested_profile = USER_PROFILES.get(profile_id)

    if active_user is None or requested_profile is None:
        # Either the requesting user or the target profile does not exist
        return "Unauthorized"

    # Determine if the active user is an admin
    is_admin = str(active_user.get("role", "")).lower() == "admin"

    # Allow access if the user is viewing their own profile or has admin privileges
    if active_user_id == profile_id or is_admin:
        return requested_profile

    # All other cases are unauthorized
    return "Unauthorized"