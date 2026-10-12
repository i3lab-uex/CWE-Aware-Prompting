# fetch_profile_info.py

from typing import Dict, Any


# Sample data structures (replace with real ones in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "bio": "Admin of the system"},
    2: {"email": "bob@example.com",   "bio": "Just a regular user"},
    3: {"email": "carol@example.com", "bio": "Another regular user"},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Dict[str, Any] | str:
    """
    Return the profile information of `view_user_id` if the requesting user
    (`logged_user_id`) is allowed to view it.  A user may view their own profile
    or, if they have the 'admin' role, any user's profile.

    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The requested user profile, or the string 'Unauthorized' if access is denied.
    """
    # Basic sanity checks
    if logged_user_id not in USERS or view_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the logged-in user's role
    user_role = USERS[logged_user_id].get("role", "")

    # Allow access if the user is viewing their own profile or has admin rights
    if logged_user_id == view_user_id or user_role.lower() == "admin":
        return USER_PROFILES[view_user_id]

    # Deny access otherwise
    return "Unauthorized"


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(fetch_profile_info(1, 2))  # Admin viewing another user
#     print(fetch_profile_info(2, 1))  # Regular user attempting to view admin
#     print(fetch_profile_info(2, 2))  # Regular user viewing own profile