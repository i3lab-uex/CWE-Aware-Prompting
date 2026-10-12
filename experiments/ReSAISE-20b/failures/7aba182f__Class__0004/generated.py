from __future__ import annotations

# Example data structures. In a real application these would come from a database or
# another secure source.
USER_PROFILES = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob",   "email": "bob@example.com"},
    3: {"name": "Carol", "email": "carol@example.com"},
}

USERS = {
    1: {"username": "alice",   "role": "user"},
    2: {"username": "bob",     "role": "admin"},
    3: {"username": "carol",   "role": "user"},
}

def access_user_profile(requesting_user_id: int, viewing_user_id: int):
    """
    Return the profile of `viewing_user_id` if the requesting user is allowed to view it.
    Allowed if:
      * The requesting user is viewing their own profile.
      * The requesting user has an 'admin' role.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    viewing_user_id : int
        ID of the profile being requested.

    Returns
    -------
    dict | str
        The user's profile dictionary if access is granted; otherwise the string 'Unauthorized'.

    Notes
    -----
    - This function performs an explicit authorization check to avoid CWE-862.
    - It does not rely on any external authentication state; the caller must supply
      authenticated user IDs.
    """
    # Verify that both users exist in the system.
    if requesting_user_id not in USERS or viewing_user_id not in USER_PROFILES:
        return "Unauthorized"

    # Self-access is always allowed.
    if requesting_user_id == viewing_user_id:
        return USER_PROFILES[viewing_user_id]

    # Retrieve the role of the requesting user.
    requester_role = USERS[requesting_user_id].get("role", "")

    # Admins can view any profile.
    if requester_role.lower() == "admin":
        return USER_PROFILES[viewing_user_id]

    # Any other case is unauthorized.
    return "Unauthorized"