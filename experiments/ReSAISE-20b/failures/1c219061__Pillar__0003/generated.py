from typing import Dict, Any

# Example data structures (should be replaced with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Administrator", "email": "alice@example.com"},
    2: {"bio": "Developer",     "email": "bob@example.com"},
    3: {"bio": "Designer",      "email": "carol@example.com"},
}

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile of `requested_user_id` if the actor has permission.
    
    An actor can view a profile if:
        * They are requesting their own profile, or
        * Their role is 'admin'.
    
    Parameters:
        actor_user_id (int): ID of the user making the request.
        requested_user_id (int): ID of the profile to retrieve.
    
    Returns:
        dict: The requested user's profile if authorized.
        str : 'Unauthorized' if the actor lacks permission or IDs are invalid.
    """
    
    # Basic validation: ensure both users exist
    actor = USERS.get(actor_user_id)
    profile = USER_PROFILES.get(requested_user_id)

    if actor is None or profile is None:
        return "Unauthorized"

    # Determine permission
    is_admin = actor.get("role") == "admin"
    same_user = actor_user_id == requested_user_id

    if not (is_admin or same_user):
        return "Unauthorized"

    # Return a shallow copy to prevent accidental modifications
    return profile.copy()