from __future__ import annotations

# Sample data structures (to be replaced with real ones in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def access_profile_details(initiator_id: int, requested_profile_id: int):
    """
    Return the profile details for `requested_profile_id` if the request is authorized.
    
    Parameters
    ----------
    initiator_id : int
        The user ID of the person making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        Profile details if authorized, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID does not exist in the system.
    """
    # Validate that both IDs exist
    if initiator_id not in USERS:
        raise ValueError(f"Initiator ID {initiator_id} does not exist.")
    if requested_profile_id not in USER_PROFILES:
        raise ValueError(f"Requested profile ID {requested_profile_id} does not exist.")

    # Determine if the initiator has permission
    is_admin = USERS[initiator_id].get("role") == "admin"
    has_access = is_admin or initiator_id == requested_profile_id

    if not has_access:
        return "Unauthorized"

    # Return a copy to avoid accidental mutation of the global data
    return USER_PROFILES[requested_profile_id].copy()