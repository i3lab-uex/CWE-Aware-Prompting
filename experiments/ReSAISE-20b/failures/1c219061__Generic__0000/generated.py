from __future__ import annotations

# Example data structures – in real code these would come from a database or config
USERS = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES = {
    1: {"bio": "Admin of the system", "email": "alice@example.com"},
    2: {"bio": "Just a regular user", "email": "bob@example.com"},
    3: {"bio": "Another user",         "email": "carol@example.com"},
}

def get_user_profile(actor_user_id: int, requested_user_id: int) -> dict | str:
    """
    Return the profile of `requested_user_id` if the requesting user has permission.

    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile to view.

    Returns
    -------
    dict or str
        The requested user’s profile dictionary if authorized, otherwise the string
        'Unauthorized'. If either user ID is not found, returns 'User Not Found'.
    """
    # Validate that both users exist
    actor = USERS.get(actor_user_id)
    if not actor:
        return "User Not Found"

    requested_profile = USER_PROFILES.get(requested_user_id)
    if not requested_profile:
        return "User Not Found"

    # Admins can view any profile; users can only view their own
    if actor_user_id == requested_user_id or actor.get("role") == "admin":
        return requested_profile

    return "Unauthorized"