from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def fetch_profile_data(requester_id: int, profile_id: int) -> Dict[str, Any] | str:
    """
    Return the requested user's profile if access is allowed.
    
    Parameters
    ----------
    requester_id : int
        The ID of the user making the request.
    profile_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        Profile data if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    KeyError
        If either requester_id or profile_id does not exist in USERS or USER_PROFILES.
    """
    # Validate existence of requester and profile
    if requester_id not in USERS:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    # Access control: owner or admin
    requester_role = USERS[requester_id].get("role")
    if requester_id == profile_id or requester_role == "admin":
        return USER_PROFILES[profile_id]
    
    # Unauthorized access
    return "Unauthorized"