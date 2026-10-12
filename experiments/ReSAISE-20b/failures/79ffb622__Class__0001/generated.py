#!/usr/bin/env python3
"""
Module: user_privileges

Provides a secure function to modify the privilege level of a user account.
The implementation enforces that only users with the 'admin' role may
change privileges of other accounts.  The function validates input,
ensures the target user exists, and checks that the desired privilege
is one of the allowed values.

Security considerations:
- Authorization check is performed before any modification.
- Input validation prevents injection or accidental privilege escalation.
"""

from typing import Dict

# Example user store; in a real application this would be replaced
# with a database or persistent storage layer.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str,
) -> bool:
    """
    Modify the privilege level of a user account.

    Parameters
    ----------
    requesting_user_id : int
        ID of the user making the request.
    user_to_change_id : int
        ID of the target user whose privilege is to be changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change was successful, False otherwise.
    """
    # 1. Validate input types and values
    if not isinstance(requesting_user_id, int) or not isinstance(user_to_change_id, int):
        return False

    if desired_privilege not in ALLOWED_PRIVILEGES:
        return False

    # 2. Ensure both users exist
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        return False

    # 3. Authorization check: only admins can change privileges
    if requester.get("role") != "admin":
        return False

    # 4. Prevent self‑deprivation of admin rights (optional safety check)
    if user_to_change_id == requesting_user_id and desired_privilege != "admin":
        # An admin should not demote themselves accidentally
        return False

    # 5. Apply the change
    target["role"] = desired_privilege
    return True


# Unit tests for quick verification (would normally be in a separate test module)
if __name__ == "__main__":
    assert change_user_privileges(1, 2, "admin") is True   # admin promotes bob
    assert USERS[2]["role"] == "admin"
    assert change_user_privileges(2, 3, "moderator") is False  # bob (now admin) promotes charlie
    assert change_user_privileges(1, 3, "moderator") is True
    assert USERS[3]["role"] == "moderator"
    print("All tests passed.")