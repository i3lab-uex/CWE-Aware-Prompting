# fetch_profile_data.py

"""
Implementation of a secure profile retrieval function.

CWE-862 (Missing Authorization) is mitigated by performing an explicit
authorization check before returning profile data.  Only the owner of a
profile or a user with an 'admin' role is permitted to access any profile.
"""

from typing import Dict, Any

# Example data structures (replace with real data sources in production)
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
    dict | str
        The profile details if access is granted; otherwise the string
        'Unauthorized'.

    Notes
    -----
    * The function performs a strict authorization check:
      - If the requester is the owner of the profile, access is granted.
      - If the requester has an 'admin' role, any profile can be accessed.
    * Any missing user or profile results in an 'Unauthorized' response
      to avoid leaking information about existence of accounts.
    """
    # Verify that both IDs exist in the data structures
    if requester_id not in USERS or profile_id not in USER_PROFILES:
        return "Unauthorized"

    # Owner check
    if requester_id == profile_id:
        return USER_PROFILES[profile_id]

    # Role-based access check
    requester_role = USERS[requester_id].get("role")
    if requester_role == "admin":
        return USER_PROFILES[profile_id]

    # If none of the above, deny access
    return "Unauthorized"


# Example usage (remove or guard with __name__ == "__main__" in production)
if __name__ == "__main__":
    print(fetch_profile_data(1, 1))   # Alice accessing own profile
    print(fetch_profile_data(2, 3))   # Admin Bob accessing Carol's profile
    print(fetch_profile_data(1, 2))   # Alice attempting to access Bob's profile