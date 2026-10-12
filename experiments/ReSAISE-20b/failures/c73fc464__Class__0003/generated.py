# fetch_profile_data.py

"""
This module implements a secure profile retrieval function.
It checks that the requester is either an administrator or the owner of the
requested profile before returning any data.  This mitigates CWE‑862 (Missing
Authorization).

Author: OpenAI ChatGPT
"""

from __future__ import annotations

# Example data structures (in a real system these would come from a database)
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"role": "admin",   "name": "Alice"},
    2: {"role": "user",    "name": "Bob"},
    3: {"role": "user",    "name": "Carol"},
}


def fetch_profile_data(requester_id: int, profile_id: int) -> dict | str:
    """
    Return the profile details for `profile_id` if the requester is authorized.
    
    Parameters
    ----------
    requester_id : int
        The user ID of the individual making the request.
    profile_id : int
        The user ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    - A user can view their own profile.
    - An administrator (role == 'admin') can view any profile.
    - All other requests are denied with an 'Unauthorized' message.

    Raises
    ------
    KeyError
        If either `requester_id` or `profile_id` does not exist in the data.
    """
    # Validate existence of requester and profile
    if requester_id not in USERS:
        raise KeyError(f"Requester ID {requester_id} does not exist.")
    if profile_id not in USER_PROFILES:
        raise KeyError(f"Profile ID {profile_id} does not exist.")

    requester_role = USERS[requester_id]["role"]

    # Authorization check
    if requester_id == profile_id or requester_role == "admin":
        return USER_PROFILES[profile_id]

    # Unauthorized access
    return "Unauthorized"