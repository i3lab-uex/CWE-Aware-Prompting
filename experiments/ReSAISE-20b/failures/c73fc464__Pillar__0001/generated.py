# -*- coding: utf-8 -*-

"""
Secure profile data fetcher.

This module defines a single function, `fetch_profile_data`, that retrieves
user profile information while enforcing proper access control.  The function
prevents CWE-284 (Improper Access Control) by ensuring that only the profile's
owner or an administrator can view a profile.

Author: OpenAI ChatGPT
"""

from typing import Dict, Any

# Sample data structures.  In a real application these would be
# fetched from a database or another persistent store.
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

def fetch_profile_data(requester_id: int, profile_id: int) -> Any:
    """
    Retrieve a user's profile data if the requester is authorized.

    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict or str
        The requested profile data if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user may view their own profile.
    - An administrator (role == 'admin') may view any profile.
    - If either the requester or the requested profile does not exist,
      access is denied and 'Unauthorized' is returned.
    """
    # Basic validation: ensure both users exist
    requester = USERS.get(requester_id)
    profile = USER_PROFILES.get(profile_id)

    if not requester or not profile:
        return "Unauthorized"

    # Access control logic
    is_owner = requester_id == profile_id
    is_admin = requester.get("role") == "admin"

    if is_owner or is_admin:
        # Return a copy to prevent accidental modification of the original data
        return dict(profile)
    else:
        return "Unauthorized"