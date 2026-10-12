#!/usr/bin/env python3
"""
Secure privilege modification utility.

The function `change_user_privileges` allows an administrator to change the
privilege level of another user.  It performs strict access checks and input
validation to prevent CWE‑284 (Improper Access Control) attacks.
"""

from typing import Dict

# Sample user store.  In a real system this would be backed by a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed privilege levels.
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def change_user_privileges(active_user_id: int,
                           affected_user_id: int,
                           updated_privilege: str) -> bool:
    """
    Change the privilege level of a user account.

    Parameters
    ----------
    active_user_id : int
        ID of the administrator attempting the change.
    affected_user_id : int
        ID of the user whose privileges are to be updated.
    updated_privilege : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # 1. Validate existence of both users
    active_user = USERS.get(active_user_id)
    affected_user = USERS.get(affected_user_id)

    if active_user is None or affected_user is None:
        return False

    # 2. Only an admin can perform the change
    if active_user["role"] != "admin":
        return False

    # 3. Prevent privilege escalation via self-modification
    if active_user_id == affected_user_id:
        return False

    # 4. Validate the requested privilege level
    if updated_privilege not in VALID_PRIVILEGES:
        return False

    # 5. Perform the update atomically
    try:
        affected_user["role"] = updated_privilege
    except Exception:
        # Any unexpected error should not expose internal state
        return False

    return True


# Example usage (uncomment to test)
if __name__ == "__main__":
    print(change_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                           # Expected: "moderator"