# -*- coding: utf-8 -*-
"""
Module providing privilege update functionality.

The implementation protects against CWE‑284 (Improper Access Control) by
ensuring that only users with the 'admin' role can modify other users'
roles. All inputs are validated and any attempt to perform an
unauthorized operation returns ``False`` instead of raising an exception.
"""

from typing import Dict

# Example USERS dictionary structure
USERS: Dict[int, Dict[str, str]] = {
    1: {"username": "alice",   "role": "admin"},
    2: {"username": "bob",     "role": "moderator"},
    3: {"username": "charlie", "role": "normal"},
}

# Allowed roles
ALLOWED_ROLES = {"normal", "moderator", "admin"}


def update_privileges(acting_user_id: int,
                      affected_user_id: int,
                      new_role: str) -> bool:
    """
    Modify the role of a user.

    Parameters
    ----------
    acting_user_id : int
        ID of the user attempting to change privileges.
    affected_user_id : int
        ID of the user whose privilege is being altered.
    new_role : str
        New role to assign.

    Returns
    -------
    bool
        ``True`` if the privilege modification succeeded,
        ``False`` otherwise.

    Notes
    -----
    * Only users with the 'admin' role can change other users' roles.
    * The function does not raise exceptions on invalid input; it simply
      returns ``False`` to signal failure.
    * The function performs no side‑effects other than updating the
      global ``USERS`` dictionary.
    """
    # Basic input validation
    if not isinstance(acting_user_id, int) or not isinstance(
        affected_user_id, int
    ):
        return False

    if new_role not in ALLOWED_ROLES:
        return False

    # Retrieve users
    acting_user = USERS.get(acting_user_id)
    affected_user = USERS.get(affected_user_id)

    # Ensure both users exist
    if acting_user is None or affected_user is None:
        return False

    # Check that the acting user has admin privileges
    if acting_user.get("role") != "admin":
        return False

    # Perform the role update
    affected_user["role"] = new_role
    return True


# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    print(update_privileges(1, 2, "admin"))   # True
    print(USERS[2]["role"])                    # admin
    print(update_privileges(3, 1, "normal"))   # False (charlie not admin)