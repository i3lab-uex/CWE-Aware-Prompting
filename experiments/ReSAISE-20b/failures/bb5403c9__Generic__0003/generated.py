# -*- coding: utf-8 -*-

"""
Utility module for user profile access control.

The function `get_profile_info` implements a simple role‑based
access control rule:
  * A user can always view their own profile.
  * An administrator (role == 'admin') can view any user's profile.
If the caller does not meet these conditions, the function returns
the string 'Unauthorized'.

The module expects two global dictionaries to exist:
  * USER_PROFILES: Mapping of user_id -> profile dict.
  * USERS: Mapping of user_id -> user metadata dict, which must
    contain at least a 'role' key.
"""

from __future__ import annotations

# Example global data structures. In a real application these
# would be provided by the surrounding system.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
}

USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
}

def get_profile_info(acting_user_id: int, viewing_user_id: int) -> dict | str:
    """
    Return the profile details for *viewing_user_id* if the request
    is authorized by *acting_user_id*.  The function checks that both
    user IDs exist in the global dictionaries, and applies the
    following rules:

    1. If the acting user is viewing their own profile, grant access.
    2. If the acting user has the role 'admin', grant access to any
       profile.
    3. Otherwise return 'Unauthorized'.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user making the request.
    viewing_user_id : int
        The ID of the profile being requested.

    Returns
    -------
    dict | str
        The profile dictionary if access is granted, otherwise the string
        'Unauthorized'.

    Notes
    -----
    - The function does not raise exceptions for missing user IDs; it
      treats them as unauthorized access.  This is a deliberate design
      choice to avoid leaking information about the existence of user
      accounts.
    - The return type is a union of `dict` and `str`.  Clients should
      inspect the result with ``isinstance(result, dict)`` to determine
      whether access succeeded.
    """
    # Quick sanity check: ensure both IDs are integers.
    if not isinstance(acting_user_id, int) or not isinstance(viewing_user_id, int):
        return "Unauthorized"

    # Retrieve acting user metadata; if not found, deny access.
    acting_user = USERS.get(acting_user_id)
    if acting_user is None:
        return "Unauthorized"

    # Check self‑viewing privilege.
    if acting_user_id == viewing_user_id:
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # Check admin privilege.
    if acting_user.get("role") == "admin":
        return USER_PROFILES.get(viewing_user_id, "Unauthorized")

    # All other cases are unauthorized.
    return "Unauthorized"