from typing import Dict, Any

# Example data structures (replace with actual data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... more profiles
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    # ... more users
}

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details for `requested_profile_id` if the request is authorized.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict | str
        The requested profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - Administrators (role == 'admin') can view any profile.
    - If either the initiator or requested user does not exist, access is denied.

    Raises
    ------
    None
        The function never raises an exception; it returns a string for all error cases.
    """
    # Validate existence of both users
    initiator = USERS.get(initiator_id)
    requested_profile = USER_PROFILES.get(requested_profile_id)

    if initiator is None or requested_profile is None:
        return "Unauthorized"

    # Check permissions
    if initiator_id == requested_profile_id or initiator.get("role") == "admin":
        return requested_profile

    return "Unauthorized"