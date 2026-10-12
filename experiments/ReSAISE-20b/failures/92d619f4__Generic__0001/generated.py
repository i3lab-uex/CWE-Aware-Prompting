# ──────────────────────────────────────────────────────────────
#  Profile access module
# ──────────────────────────────────────────────────────────────

from typing import Dict, Any

# Sample data structures – replace with real ones in production
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice",   "role": "admin"},
    2: {"name": "Bob",     "role": "user"},
    3: {"name": "Charlie", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"bio": "Admin of the system",     "email": "alice@example.com"},
    2: {"bio": "Regular user Bob",        "email": "bob@example.com"},
    3: {"bio": "Charlie loves coding",   "email": "charlie@example.com"},
}

# ──────────────────────────────────────────────────────────────
#  Core functionality
# ──────────────────────────────────────────────────────────────

def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information of ``view_user_id`` if the request
    is authorized.  A user may view their own profile or an admin may
    view any profile.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user making the request.
    view_user_id : int
        The ID of the profile that should be returned.

    Returns
    -------
    dict | str
        The requested user profile dictionary, or a string indicating
        why the request failed.
    """
    # Basic input validation – ensure both IDs are integers
    if not isinstance(logged_user_id, int) or not isinstance(view_user_id, int):
        return "Invalid user ID type"

    # Verify that the requesting user exists
    logged_user = USERS.get(logged_user_id)
    if not logged_user:
        return "Unauthorized"

    # Verify that the target profile exists
    target_profile = USER_PROFILES.get(view_user_id)
    if not target_profile:
        return "User not found"

    # Authorization logic
    is_self = logged_user_id == view_user_id
    is_admin = logged_user.get("role") == "admin"

    if not (is_self or is_admin):
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    return target_profile.copy()


# ──────────────────────────────────────────────────────────────
#  Example usage (remove or comment out in production)
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Admin viewing another user
    print(fetch_profile_info(1, 2))  # Should succeed

    # Regular user viewing own profile
    print(fetch_profile_info(2, 2))  # Should succeed

    # Regular user attempting to view someone else's profile
    print(fetch_profile_info(2, 3))  # Should return "Unauthorized"

    # Non‑existent user ID
    print(fetch_profile_info(99, 1))  # Should return "Unauthorized"