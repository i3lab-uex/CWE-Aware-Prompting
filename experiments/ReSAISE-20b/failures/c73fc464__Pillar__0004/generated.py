# fetch_profile_data.py

from typing import Dict, Any

# Example data structures (replace with actual application data)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"}
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"}
}


def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if the requester has permission.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict or str
        Profile details if access is granted, otherwise the string 'Unauthorized'.
    """
    # Validate existence of requester and target profiles
    if requester_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Check if requester is requesting their own profile
    if requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Fetch the role of the requester
    requester_role = USERS.get(requester_id, {}).get("role", "")

    # Admins can view any profile
    if requester_role.lower() == "admin":
        return USER_PROFILES[profile_id]

    # All other cases are unauthorized
    return "Unauthorized"