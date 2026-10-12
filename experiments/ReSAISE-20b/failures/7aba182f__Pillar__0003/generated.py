from __future__ import annotations

# Sample data structures. In a real application these would come from a database or external source.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}


def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> dict | str:
    """
    Return the profile of *viewing_user_id* if the requesting user is allowed to view it.
    Authorization rules:
        - A user can view their own profile.
        - An administrator (role == 'admin') can view any profile.
    If the user is not authorized or if either ID does not exist, return 'Unauthorized'.
    """
    # Validate that both user IDs exist
    requester = USERS.get(requesting_user_id)
    target_profile = USER_PROFILES.get(viewing_user_id)

    if requester is None or target_profile is None:
        return "Unauthorized"

    # Allow access if the user is requesting their own profile
    if requesting_user_id == viewing_user_id:
        return target_profile

    # Allow access if the requester has an admin role
    if requester.get("role") == "admin":
        return target_profile

    # All other cases are unauthorized
    return "Unauthorized"