from __future__ import annotations

from typing import Any, Dict

# Example data structures – in real code these would come from a database or other source.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Dict[str, Any] | str:
    """
    Return the profile information for ``view_user_id`` if the requesting user
    (``logged_user_id``) is allowed to view it.

    A user can view their own profile. An admin (role == "admin") can view any
    profile.

    Parameters
    ----------
    logged_user_id : int
        ID of the user making the request.
    view_user_id : int
        ID of the profile to be viewed.

    Returns
    -------
    dict | str
        The requested user's profile dictionary, or the string "Unauthorized"
        if access is denied.

    Raises
    ------
    KeyError
        If either ``logged_user_id`` or ``view_user_id`` is not present in the
        data structures.
    """
    # Validate that both users exist
    if logged_user_id not in USERS:
        raise KeyError(f"Logged user ID {logged_user_id} does not exist.")
    if view_user_id not in USER_PROFILES:
        raise KeyError(f"Profile for user ID {view_user_id} does not exist.")

    # Determine if the logged-in user is an admin
    is_admin = USERS[logged_user_id].get("role") == "admin"

    # Authorization logic
    if logged_user_id == view_user_id or is_admin:
        return USER_PROFILES[view_user_id]
    else:
        return "Unauthorized"