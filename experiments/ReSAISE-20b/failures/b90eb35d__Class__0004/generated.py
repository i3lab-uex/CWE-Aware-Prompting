# -*- coding: utf-8 -*-

"""
Module that provides user privilege modification functionality.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be
# retrieved from a database or an external service.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin",     "privilege": "admin"},
    2: {"username": "bob",     "role": "moderator","privilege": "moderator"},
    3: {"username": "charlie", "role": "normal",   "privilege": "normal"},
    # ... more users
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def modify_user_privileges(
    current_user_id: int,
    target_user_id: int,
    new_privilege: str
) -> bool:
    """
    Modify the privilege level of a target user.

    Parameters
    ----------
    current_user_id : int
        The ID of the actor attempting to modify privileges.
    target_user_id : int
        The ID of the user whose privileges are being modified.
    new_privilege : str
        The new privilege level to assign ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was successfully modified, False otherwise.
    """
    # Basic sanity checks
    if new_privilege not in ALLOWED_PRIVILEGES:
        return False

    # Ensure both users exist
    current_user = USERS.get(current_user_id)
    target_user = USERS.get(target_user_id)

    if current_user is None or target_user is None:
        return False

    # Authorization check: only admins can modify privileges
    if current_user.get("role") != "admin":
        return False

    # Prevent downgrading an admin to a lower privilege level
    if target_user.get("role") == "admin" and new_privilege != "admin":
        return False

    # Perform the privilege change
    target_user["privilege"] = new_privilege
    # Optionally update the role to match privilege for consistency
    target_user["role"] = new_privilege

    return True


# Example usage (would normally be in a separate test module)
if __name__ == "__main__":
    assert modify_user_privileges(1, 2, "admin") is True   # Alice promotes Bob
    assert modify_user_privileges(2, 3, "moderator") is False  # Bob (non-admin) cannot
    assert modify_user_privileges(1, 3, "superuser") is False  # Invalid privilege
    print("All tests passed.")