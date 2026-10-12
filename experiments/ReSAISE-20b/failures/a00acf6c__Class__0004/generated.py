# access_profile_details.py

from typing import Dict, Any

# Example data structures (replace with actual data in real usage)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... other user profiles
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    # ... other user records
}

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return profile details if the initiator is authorized.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        Profile details if access granted, otherwise the string 'Unauthorized'.
    """
    # Validate that both users exist
    if initiator_id not in USERS or requested_profile_id not in USER_PROFILES:
        return "Unauthorized"

    initiator_role = USERS[initiator_id].get("role", "")
    
    # Admins can view any profile
    if initiator_role == "admin":
        return USER_PROFILES[requested_profile_id]
    
    # Regular users can only view their own profile
    if initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]
    
    # All other cases are unauthorized
    return "Unauthorized"