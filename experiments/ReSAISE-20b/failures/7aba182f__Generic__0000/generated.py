from __future__ import annotations

# Example data structures (replace with actual data in production)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob",   "role": "admin"},
    3: {"username": "carol", "role": "user"},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int):
    """
    Return the profile of `viewing_user_id` if `requesting_user_id`
    is either the same user or has an admin role.  Otherwise return
    'Unauthorized'.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user profile dictionary or the string 'Unauthorized'.
    """
    # Validate that both IDs are integers
    if not isinstance(requesting_user_id, int) or not isinstance(viewing_user_id, int):
        return "Unauthorized"

    # Retrieve the requesting user's role
    requester = USERS.get(requesting_user_id)
    if not requester:
        return "Unauthorized"

    # Permission check: same user or admin role
    if requesting_user_id == viewing_user_id or requester.get("role") == "admin":
        profile = USER_PROFILES.get(viewing_user_id)
        if profile is None:
            # Profile not found: treat as unauthorized to avoid leaking info
            return "Unauthorized"
        return profile

    # If none of the conditions are met, deny access
    return "Unauthorized"