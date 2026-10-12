# Assuming these dictionaries are defined elsewhere in the application.
# They could be imported from a config or database module.
# For this example, we provide minimal mock definitions.

USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Eve",   "email": "eve@example.com"}
}

USERS = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"}
}


def fetch_profile_data(requester_id: int, profile_id: int):
    """
    Retrieve a user profile if the requester has permission.

    Parameters
    ----------
    requester_id : int
        ID of the user making the request.
    profile_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted; otherwise the string
        'Unauthorized'.
    """
    # Validate that both IDs exist in the system.
    if requester_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Self‑access: user can view their own profile.
    if requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Admin access: only admins can view others' profiles.
    if USERS.get(requester_id, {}).get("role") == "admin":
        return USER_PROFILES[profile_id]

    # All other cases are forbidden.
    return "Unauthorized"