from typing import Dict, Any

# Sample data structures (replace with real ones in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Return the requested user profile if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        Profile data dictionary if authorized, otherwise the string 'Unauthorized'.
    """
    # Verify that both IDs exist in our data stores
    if requester_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve user roles
    requester_role = USERS[requester_id].get("role", "")

    # Authorization logic:
    # - A user can view their own profile
    # - An admin can view any profile
    if requester_id == profile_id or requester_role.lower() == "admin":
        return USER_PROFILES[profile_id]

    # Any other case is not authorized
    return "Unauthorized"