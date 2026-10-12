# -*- coding: utf-8 -*-

"""
Utility to retrieve user profile details with role-based access control.
"""

from typing import Dict, Any

# Example data structures. In a real application these would come from a database.
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
}

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details of *requested_profile_id* if the request is authorized.
    
    An access is granted when:
        1. The initiator is requesting their own profile.
        2. The initiator has an 'admin' role.

    Parameters
    ----------
    initiator_id : int
        User ID of the person making the request.
    requested_profile_id : int
        User ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string 'Unauthorized'.
    
    Notes
    -----
    - The function performs no I/O and is safe for use in concurrent environments.
    - It checks that both user IDs exist; missing users result in 'Unauthorized'.
    """
    # Verify that both the initiator and requested user exist
    if initiator_id not in USERS or requested_profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Same user or admin can view the profile
    if initiator_id == requested_profile_id:
        return USER_PROFILES[requested_profile_id]

    initiator_role = USERS.get(initiator_id, {}).get("role", "")
    if initiator_role.lower() == "admin":
        return USER_PROFILES[requested_profile_id]

    # All other cases are forbidden
    return "Unauthorized"

# Example usage (for testing purposes)
if __name__ == "__main__":
    print(access_profile_details(1, 2))   # Admin viewing Bob's profile
    print(access_profile_details(2, 2))   # User viewing own profile
    print(access_profile_details(2, 3))   # Unauthorized: Bob trying to view Carol