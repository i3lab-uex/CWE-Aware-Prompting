from typing import Dict, Any

# Example data structures (replace with real data in production)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, str] = {
    1: "user",
    2: "admin",
    3: "user",
}

def view_user_profile(current_user_id: int, target_user_id: int) -> Any:
    """
    Return the profile information for `target_user_id` if the caller is authorized.

    Authorization rules:
        * A user may view their own profile.
        * An admin (role == "admin") may view any user's profile.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor making the request.
    target_user_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict or str
        The target user's profile dictionary if authorized,
        otherwise the string 'Unauthorized'.
    """
    # Validate that both users exist
    if current_user_id not in USERS or target_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Admin check
    if USERS.get(current_user_id) == "admin":
        return USER_PROFILES[target_user_id]

    # Self‑view check
    if current_user_id == target_user_id:
        return USER_PROFILES[target_user_id]

    # No other permissions allowed
    return "Unauthorized"