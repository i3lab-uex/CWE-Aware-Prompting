from typing import Dict, Any

# Sample data structures (these would normally be populated elsewhere)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    # ... more profiles ...
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "user"},
    # ... more users ...
}

def get_user_profile(actor_user_id: int, requested_user_id: int) -> Any:
    """
    Return the profile of `requested_user_id` if the actor is authorized.
    
    An actor is authorized if:
      - They are an admin (`role == 'admin'` in USERS).
      - OR they request their own profile.
      
    Parameters
    ----------
    actor_user_id : int
        ID of the user making the request.
    requested_user_id : int
        ID of the profile being requested.
    
    Returns
    -------
    dict | str
        The user's profile dictionary if authorized, otherwise the string 'Unauthorized'.
    
    Raises
    ------
    KeyError
        If either `actor_user_id` or `requested_user_id` does not exist in the data structures.
    """
    
    # Ensure both users exist
    if actor_user_id not in USERS:
        raise KeyError(f"Actor user ID {actor_user_id} does not exist.")
    if requested_user_id not in USER_PROFILES:
        raise KeyError(f"Requested user ID {requested_user_id} does not exist.")
    
    actor = USERS[actor_user_id]
    
    # Check authorization
    is_admin = actor.get("role") == "admin"
    is_self = actor_user_id == requested_user_id
    
    if not (is_admin or is_self):
        return "Unauthorized"
    
    # Return a copy to avoid accidental modifications
    return dict(USER_PROFILES[requested_user_id])