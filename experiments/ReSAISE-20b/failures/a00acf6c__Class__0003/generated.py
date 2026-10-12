# access_profile_details.py

"""
Access control for viewing user profiles.

The function ensures that only the owner of a profile or an administrator
can retrieve profile details.  It protects against CWE‑862: Missing
Authorization.
"""

from typing import Dict, Any

# Example data structures – in a real application these would be loaded
# from a database or other persistent store.
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
    Return the profile details for `requested_profile_id` if the request is
    authorized.  Otherwise return the string 'Unauthorized'.

    Parameters
    ----------
    initiator_id : int
        The user ID of the individual making the request.
    requested_profile_id : int
        The user ID whose profile is being requested.

    Returns
    -------
    dict | str
        Profile details if access is granted, otherwise 'Unauthorized'.
    """
    # Quick existence check – missing data should not grant access.
    if initiator_id not in USERS or requested_profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Fetch the initiator's role.
    initiator_role = USERS[initiator_id].get("role", "")

    # Authorization logic:
    # 1. The user can view their own profile.
    # 2. Administrators can view any profile.
    if initiator_id == requested_profile_id or initiator_role.lower() == "admin":
        return USER_PROFILES[requested_profile_id]

    # All other cases are unauthorized.
    return "Unauthorized"