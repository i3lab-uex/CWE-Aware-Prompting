# -*- coding: utf-8 -*-
"""
Profile access control module.

This module provides a single function, `get_profile_info`, which enforces
proper access control based on user roles.  The implementation follows the
CWE‑284 (Improper Access Control) guidance to ensure that only authorized
parties can view a user's profile.

The module is intentionally minimal and self‑contained; no external
dependencies are required.
"""

from typing import Dict, Any

# Example data structures.  In a real application these would be replaced
# by database queries or an ORM layer.
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


def get_profile_info(acting_user_id: int, viewing_user_id: int) -> Any:
    """
    Return profile information for `viewing_user_id` if the request is
    authorized by the acting user.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict or str
        The user's profile dictionary if access is granted, otherwise the
        string 'Unauthorized'.

    Notes
    -----
    * Administrators (role == "admin") can view any profile.
    * Regular users may only view their own profile.
    * The function performs defensive checks to guard against missing
      entries in the global dictionaries.  If either user ID is unknown,
      the function treats it as an unauthorized request.

    Security
    --------
    This implementation explicitly checks the role before returning data,
    thereby preventing accidental leakage of sensitive information.
    """
    # Verify that both user IDs exist in the system
    if acting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Retrieve roles and profile
    acting_user = USERS[acting_user_id]
    profile = USER_PROFILES.get(viewing_user_id)

    # Allow access if the acting user is an admin
    if acting_user.get("role") == "admin":
        return profile

    # Regular users may only view their own profile
    if acting_user_id == viewing_user_id:
        return profile

    # All other cases are denied
    return "Unauthorized"


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(get_profile_info(1, 2))  # Admin viewing Bob's profile
    print(get_profile_info(2, 1))  # Bob trying to view Alice's profile
    print(get_profile_info(2, 2))  # Bob viewing his own profile