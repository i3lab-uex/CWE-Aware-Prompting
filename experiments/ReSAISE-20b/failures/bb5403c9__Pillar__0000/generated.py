# -*- coding: utf-8 -*-
"""
Implements an access‑controlled profile viewer.

The function `get_profile_info` checks that the acting user is either
the owner of the profile or has an administrative role before returning
profile data.  If the check fails, it returns the string 'Unauthorized'.

Security Note:
- The implementation follows CWE‑284 guidelines by ensuring that
  only authorized users can access profile data.
- All input parameters are validated for type and existence before
  processing to avoid unexpected errors or information leakage.
"""

from __future__ import annotations

# Example data structures (replace with real data in production)
USER_PROFILES: dict[int, dict] = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS: dict[int, dict] = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> dict | str:
    """
    Return profile information if the acting user is authorized.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        Profile data if access is granted; otherwise the string
        'Unauthorized'.

    Raises
    ------
    ValueError
        If either user ID is not an integer or does not exist in the data.
    """
    # Validate types
    if not isinstance(acting_user_id, int) or not isinstance(viewing_user_id, int):
        raise ValueError("User IDs must be integers.")

    # Validate existence
    if acting_user_id not in USERS:
        raise ValueError(f"Acting user ID {acting_user_id} does not exist.")
    if viewing_user_id not in USER_PROFILES:
        raise ValueError(f"Viewing user ID {viewing_user_id} does not exist.")

    # Check ownership or admin role
    if acting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    acting_role = USERS.get(acting_user_id, {}).get("role", "")
    if acting_role == "admin":
        return USER_PROFILES[viewing_user_id]

    # Access denied
    return "Unauthorized"