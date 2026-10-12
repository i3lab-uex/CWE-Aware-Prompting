# access_profile_details.py

from typing import Dict, Any

# Sample data structures (replace with actual application data)
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
    Return the profile details of a user if the request is authorized.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        Profile details if access is granted, otherwise the string 'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not present in the system.
    TypeError
        If the provided IDs are not integers.
    """
    # Basic type validation to avoid injection or malformed input
    if not isinstance(initiator_id, int) or not isinstance(requested_profile_id, int):
        raise TypeError("User IDs must be integers.")

    # Verify that both users exist
    if initiator_id not in USERS:
        raise ValueError(f"Initiator ID {initiator_id} does not exist.")
    if requested_profile_id not in USER_PROFILES:
        raise ValueError(f"Requested profile ID {requested_profile_id} does not exist.")

    # Determine initiator role
    initiator_role = USERS[initiator_id].get("role", "user")

    # Authorization logic:
    # - Admins can view any profile
    # - Regular users can only view their own profile
    if initiator_role == "admin" or initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]

    # If none of the above, deny access
    return "Unauthorized"