from typing import Any, Dict

# Sample data structures (replace with actual data in real usage)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def see_user_profile(current_id: int, target_id: int) -> Any:
    """
    Return the profile of `target_id` if the requesting user is allowed to view it.
    
    A user may view their own profile or any profile if they have the 'admin' role.
    
    Parameters
    ----------
    current_id : int
        ID of the user making the request.
    target_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile if authorized, otherwise the string 'Unauthorized'.
    """
    # Validate that both IDs exist in the system
    if current_id not in USERS or target_id not in USER_PROFILES:
        return "Unauthorized"

    # Determine the role of the current user
    current_role = USERS.get(current_id, {}).get("role", "user")

    # Access control: allow if same user or admin
    if current_id == target_id or current_role.lower() == "admin":
        return USER_PROFILES[target_id]

    # Default: deny access
    return "Unauthorized"