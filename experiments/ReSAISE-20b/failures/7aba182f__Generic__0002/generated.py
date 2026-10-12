# access_user_profile.py

from typing import Dict, Any

# Example data structures. In real usage these would be populated elsewhere.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"},
    3: {"name": "Charlie", "email": "charlie@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"username": "alice", "role": "user"},
    2: {"username": "bob", "role": "admin"},
    3: {"username": "charlie", "role": "user"},
}


def access_user_profile(requesting_user_id: int, viewing_user_id: int) -> Any:
    """
    Grants access to a user profile if the requesting user is either
    the owner of the profile or has an 'admin' role.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict or str
        The user profile dictionary if access is allowed,
        otherwise the string 'Unauthorized'.

    Notes
    -----
    - If either user ID does not exist in the respective dictionaries,
      access is denied.
    - Role names are case-sensitive; only 'admin' grants elevated access.
    """
    # Validate existence of both users
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch roles and profile
    requesting_user = USERS[requesting_user_id]
    if (
        requesting_user_id == viewing_user_id
        or requesting_user.get("role") == "admin"
    ):
        return USER_PROFILES[viewing_user_id]

    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(access_user_profile(1, 1))   # Own profile: allowed
    print(access_user_profile(2, 3))   # Admin viewing another: allowed
    print(access_user_profile(1, 2))   # Regular user viewing admin's profile: denied