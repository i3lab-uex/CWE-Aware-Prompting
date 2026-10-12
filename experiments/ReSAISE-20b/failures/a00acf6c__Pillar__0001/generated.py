# -*- coding: utf-8 -*-

"""
Access control module for user profiles.
"""

from typing import Dict, Any

# Example data structures (replace with actual application data)
USER_PROFILES: Dict[int, Dict[str, Any]] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def access_profile_details(initiator_id: int, requested_profile_id: int) -> Any:
    """
    Return the profile details for `requested_profile_id` if the request is authorized.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict or str
        The requested profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - Users can view only their own profiles.
    - Administrators (role == 'admin') can view any profile.
    - The function performs minimal validation and returns a generic
      'Unauthorized' string to avoid leaking information about existing users.
    """
    # Basic type validation
    if not isinstance(initiator_id, int) or not isinstance(requested_profile_id, int):
        return "Unauthorized"

    # Retrieve initiator information
    initiator = USERS.get(initiator_id)
    if not initiator:
        return "Unauthorized"

    # Check permissions
    is_admin = initiator.get("role") == "admin"
    if not (is_admin or initiator_id == requested_profile_id):
        return "Unauthorized"

    # Retrieve the profile
    profile = USER_PROFILES.get(requested_profile_id)
    if not profile:
        return "Unauthorized"

    # Return a copy to prevent accidental mutation
    return dict(profile)