from typing import Dict, Any

# Sample data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return the profile of `viewing_user_id` if the request is authorized.

    Parameters
    ----------
    acting_user_id : int
        The user ID of the person making the request.
    viewing_user_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The profile dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    # Verify both users exist
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return "Unauthorized"

    # Admins can view any profile
    if acting_user.get("role") == "admin":
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # Regular users can only view their own profile
    if acting_user_id == viewing_user_id:
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # If none of the above, deny access
    return "Unauthorized"