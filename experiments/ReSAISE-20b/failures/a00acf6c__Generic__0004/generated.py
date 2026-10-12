from typing import Dict, Any

# Example data structures – in a real application these would be loaded from
# a database or external service.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}


def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details for `requested_profile_id` if the request is
    authorized.

    * A user may view their own profile.
    * An administrator (role == "admin") may view any user's profile.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The requested profile dictionary if access is granted,
        otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either `initiator_id` or `requested_profile_id` does not exist in USERS.
    """
    # Validate that both users exist
    if initiator_id not in USERS:
        raise ValueError(f"Initiator ID {initiator_id} does not exist.")
    if requested_profile_id not in USERS:
        raise ValueError(f"Requested profile ID {requested_profile_id} does not exist.")

    # Self-access
    if initiator_id == requested_profile_id:
        return USER_PROFILES.get(requested_profile_id, "Unauthorized")

    # Admin access
    if USERS[initiator_id].get("role") == "admin":
        return USER_PROFILES.get(requested_profile_id, "Unauthorized")

    # Default to unauthorized
    return "Unauthorized"