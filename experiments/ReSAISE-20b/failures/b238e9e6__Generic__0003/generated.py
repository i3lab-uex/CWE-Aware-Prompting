# -*- coding: utf-8 -*-
"""
Utility module for user privilege management.
"""

from typing import Dict

# Example in-memory store of users. In a real application this would
# be replaced by a database or persistent storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed roles, defined in order of increasing privilege.
ALLOWED_ROLES = ("normal", "moderator", "admin")


def update_privileges(acting_user_id: int, affected_user_id: int, new_role: str) -> bool:
    """
    Modify the privilege level of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to perform the change.
    affected_user_id : int
        ID of the user whose role will be altered.
    new_role : str
        Desired role for the affected user.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Notes
    -----
    - Only users with role 'admin' are allowed to change roles.
    - The new_role must be one of the predefined ALLOWED_ROLES.
    - Users cannot change their own role to a higher privilege than they currently hold.
    """
    # Quick existence checks
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    if acting_user is None or affected_user is None:
        return False

    # Only admins can change roles
    if acting_user["role"] != "admin":
        return False

    # Validate the new role
    if new_role not in ALLOWED_ROLES:
        return False

    # Prevent privilege escalation on self (optional security measure)
    if acting_user_id == affected_user_id and new_role != acting_user["role"]:
        return False

    # Apply the change
    affected_user["role"] = new_role
    return True


# Example usage (uncomment to test)
if __name__ == "__main__":
    print(update_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                      # Expected: "moderator"