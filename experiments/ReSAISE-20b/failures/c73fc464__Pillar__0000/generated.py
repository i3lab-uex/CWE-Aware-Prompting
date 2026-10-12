from __future__ import annotations

# Sample data structures (in real usage these would be populated elsewhere)
USER_PROFILES: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: dict[int, dict] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}


def fetch_profile_data(requester_id: int, profile_id: int) -> dict | str:
    """
    Return the requested user profile if the requester has permission.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.
    """
    # Verify that both users exist
    requester = USERS.get(requester_id)
    profile = USER_PROFILES.get(profile_id)

    if requester is None or profile is None:
        # Either the requester or target does not exist
        return "Unauthorized"

    role = requester.get("role", "").lower()

    # Admins can access any profile
    if role == "admin":
        return profile

    # Regular users may only access their own profile
    if requester_id == profile_id:
        return profile

    # All other cases are unauthorized
    return "Unauthorized"