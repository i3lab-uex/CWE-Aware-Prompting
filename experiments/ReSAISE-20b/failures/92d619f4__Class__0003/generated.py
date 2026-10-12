from typing import Dict, Any

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Administrator",   "email": "alice@example.com"},
    2: {"bio": "Regular user",    "email": "bob@example.com"},
    3: {"bio": "Another user",    "email": "carol@example.com"},
}

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information of `view_user_id` if the requesting user
    is allowed to see it. The user can view their own profile or any profile
    if they have an admin role.

    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Access control is enforced to mitigate CWE-862 (Missing Authorization).
    - The function gracefully handles missing user IDs by returning
      'Unauthorized'.
    """
    # Check if both users exist in the system
    logged_user = USERS.get(logged_user_id)
    target_profile = USER_PROFILES.get(view_user_id)

    if logged_user is None or target_profile is None:
        return "Unauthorized"

    # Allow self-view
    if logged_user_id == view_user_id:
        return target_profile

    # Allow admin role to view any profile
    if logged_user.get("role") == "admin":
        return target_profile

    # All other cases are unauthorized
    return "Unauthorized"