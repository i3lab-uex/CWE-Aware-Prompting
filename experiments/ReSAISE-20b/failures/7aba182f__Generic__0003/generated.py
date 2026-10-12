# ──────────────────────────────────────────────────────────────
#  Access control for user profiles
# ──────────────────────────────────────────────────────────────

from typing import Dict, Any, Union


# Example data structures – in real use these would be populated
# from a database or external source.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}


def access_user_profile(
    requesting_user_id: int,
    viewing_user_id: int
) -> Union[Dict[str, Any], str]:
    """
    Return the requested user's profile if the requesting user is
    either the owner of the profile or has an 'admin' role.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.
    """
    # Validate that both users exist
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the role of the requesting user
    requester_role = USERS[requesting_user_id].get("role", "user")

    # Grant access if the requester is the owner or an admin
    if requesting_user_id == viewing_user_id or requester_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id]

    # All other cases are denied
    return "Unauthorized"