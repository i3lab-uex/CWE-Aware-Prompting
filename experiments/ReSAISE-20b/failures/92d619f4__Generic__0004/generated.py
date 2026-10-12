# -*- coding: utf-8 -*-
"""
Utility module to fetch user profile information with access control.

The module expects two global dictionaries:
    - USERS:   maps a user_id to a dict containing at least the key 'role'
               (possible values: 'admin' or 'user').
    - USER_PROFILES: maps a user_id to the profile data that should be returned.

The function fetch_profile_info implements the following rules:

1. A user can always view their own profile.
2. An admin (role == 'admin') can view any user's profile.
3. All other requests are denied and the string "Unauthorized" is returned.

The function is defensive: it handles missing user IDs gracefully by
returning "Unauthorized".
"""

from typing import Any, Dict

# Example data structures. In real usage these would be imported from
# another module or fetched from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "role": "admin"},
    2: {"name": "Bob",   "role": "user"},
    3: {"name": "Carol", "role": "user"},
}

USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"email": "alice@example.com", "age": 30},
    2: {"email": "bob@example.com",   "age": 25},
    3: {"email": "carol@example.com", "age": 28},
}


def fetch_profile_info(logged_user_id: int, view_user_id: int) -> Any:
    """
    Return the profile information for ``view_user_id`` if the requester
    identified by ``logged_user_id`` has permission.

    Parameters
    ----------
    logged_user_id : int
        The ID of the user initiating the request.
    view_user_id : int
        The ID of the profile to be viewed.

    Returns
    -------
    dict or str
        The requested user profile dictionary if access is granted,
        otherwise the string "Unauthorized".
    """
    # Validate that both user IDs exist in our data stores.
    logged_user = USERS.get(logged_user_id)
    target_profile = USER_PROFILES.get(view_user_id)

    if logged_user is None or target_profile is None:
        # Either the requester or the requested profile does not exist.
        return "Unauthorized"

    # Rule 1: a user can view their own profile
    if logged_user_id == view_user_id:
        return target_profile

    # Rule 2: admins can view any profile
    if logged_user.get("role") == "admin":
        return target_profile

    # Rule 3: all other cases are denied
    return "Unauthorized"


# If this module is run directly, perform a quick demonstration.
if __name__ == "__main__":
    tests = [
        (1, 2),  # admin viewing another user
        (2, 2),  # normal user viewing self
        (2, 1),  # normal user attempting to view admin profile
        (4, 1),  # non‑existent logged user
        (1, 5),  # non‑existent target profile
    ]

    for logged_id, view_id in tests:
        result = fetch_profile_info(logged_id, view_id)
        print(f"fetch_profile_info({logged_id}, {view_id}) -> {result!r}")