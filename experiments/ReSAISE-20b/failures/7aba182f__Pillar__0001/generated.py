from __future__ import annotations

# Sample data structures (replace with actual data in production)
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
    Return the profile of `viewing_user_id` if the requesting user is authorized.
    
    Authorization rules:
        * A user may view their own profile.
        * An administrator (role == 'admin') may view any profile.
    
    If the user is not found or lacks permission, returns 'Unauthorized'.
    """
    # Retrieve requesting user data; treat missing users as unauthorized
    requester = USERS.get(requesting_user_id)
    if not requester:
        return "Unauthorized"

    # Determine if the request is permitted
    is_self = requesting_user_id == viewing_user_id
    is_admin = requester.get("role") == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Retrieve the requested profile; if not found, treat as unauthorized
    profile = USER_PROFILES.get(viewing_user_id)
    if not profile:
        return "Unauthorized"

    # Return a copy to avoid accidental mutation of the stored data
    return profile.copy()