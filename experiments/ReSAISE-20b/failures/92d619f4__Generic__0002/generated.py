# fetch_profile_info.py

from typing import Dict, Any


# Example data structures (replace with real ones in your application)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id: { 'name': str, 'role': str }
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    # user_id: profile data
    1: {"email": "alice@example.com", "bio": "Administrator"},
    2: {"email": "bob@example.com",   "bio": "Developer"},
    3: {"email": "carol@example.com", "bio": "Designer"},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information for *view_user_id* if the caller (*logged_user_id*)
    is allowed to see it.

    Permissions:
        * A user can view their own profile.
        * An admin (role == 'admin') can view any profile.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The requested profile dictionary if authorized, otherwise the string
        'Unauthorized'.

    Raises
    ------
    KeyError
        If either *logged_user_id* or *view_user_id* does not exist in the data.
    """
    # Validate that both users exist
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Profile for user ID {view_user_id} does not exist.")

    # Determine if the logged-in user is an admin
    is_admin = USERS[logged_user_id].get("role") == "admin"

    # Authorization check
    if logged_user_id == view_user_id or is_admin:
        return USER_PROFILES[view_user_id]
    else:
        return "Unauthorized"