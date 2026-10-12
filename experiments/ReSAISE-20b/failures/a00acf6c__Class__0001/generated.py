from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ...
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    # ...
}


def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details if the initiator is authorized to view them.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        Profile dictionary if access granted; otherwise the string 'Unauthorized'.

    Notes
    -----
    - Users can view their own profiles.
    - Administrators (role == 'admin') can view any profile.
    - All other attempts are denied to prevent CWE-862 vulnerabilities.
    """
    # Validate that both users exist
    if initiator_id not in USERS or requested_profile_id not in USER_PROFILES:
        return "Unauthorized"

    initiator = USERS[initiator_id]
    # Allow if the user is requesting their own profile
    if initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]

    # Allow if the initiator is an administrator
    if initiator.get("role") == "admin":
        return USER_PROFILES[requested_profile_id]

    # All other cases are unauthorized
    return "Unauthorized"