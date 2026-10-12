# -*- coding: utf-8 -*-
"""
Utility to retrieve user profile details with proper access control.
"""

from typing import Dict, Any

# Example data structures. In real applications these would be
# populated from a database or external service.
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

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details for *requested_profile_id* if the caller
    (identified by *initiator_id*) has sufficient privileges.

    Parameters
    ----------
    initiator_id : int
        User ID of the individual making the request.
    requested_profile_id : int
        User ID whose profile is being requested.

    Returns
    -------
    dict or str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Regular users can only access their own profile.
    - Administrators (role == 'admin') may access any profile.
    - The function is defensive: missing user IDs or profiles result in
      an 'Unauthorized' response instead of raising exceptions.
    """
    # Validate that both IDs exist in the system
    initiator = USERS.get(initiator_id)
    requested_profile = USER_PROFILES.get(requested_profile_id)

    if initiator is None or requested_profile is None:
        return "Unauthorized"

    # Determine access rights
    if initiator_id == requested_profile_id:
        return requested_profile

    # Check for admin privileges
    if initiator.get("role") == "admin":
        return requested_profile

    # Default: deny access
    return "Unauthorized"

# Example usage (for testing purposes only):
if __name__ == "__main__":
    print(access_profile_details(1, 1))   # Own profile -> allowed
    print(access_profile_details(2, 3))   # Admin accessing another -> allowed
    print(access_profile_details(1, 2))   # Regular user accessing others -> denied