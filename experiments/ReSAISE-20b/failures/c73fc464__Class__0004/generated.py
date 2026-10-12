# -*- coding: utf-8 -*-
"""
Utility module to fetch user profile data with proper authorization checks.

The function ``fetch_profile_data`` ensures that only the profile owner or an
administrator can retrieve a profile. It mitigates CWE-862 (Missing
Authorization) by performing explicit role checks before returning sensitive
information.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from a
# database or another persistent store.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "user"},
    2: {"role": "admin"},
    3: {"role": "user"},
}

def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Retrieve the profile data for ``profile_id`` if the requester has
    sufficient privileges.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    * The function first checks that both the requester and the requested profile
      exist in the system. If either is missing, 'Unauthorized' is returned.
    * A user may view their own profile. Administrators may view any profile.
    """
    # Validate existence of requester and target profile
    if requester_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Allow self-access
    if requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Allow admin access
    if USERS.get(requester_id, {}).get("role") == "admin":
        return USER_PROFILES[profile_id]

    # Default: access denied
    return "Unauthorized"

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(fetch_profile_data(1, 1))   # Alice accessing own profile
    print(fetch_profile_data(2, 3))   # Admin accessing Carol's profile
    print(fetch_profile_data(1, 2))   # Alice trying to access Bob's profile