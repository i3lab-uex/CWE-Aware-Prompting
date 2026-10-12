# -*- coding: utf-8 -*-
"""
Implementation of `alter_user_permissions` with proper access control.
The function ensures that only users with 'admin' privilege can change the
privilege level of other users.  It also validates that the new privilege
level is one of the allowed values.
"""

from typing import Dict

# Sample in‑memory user store.  In a real application this would be
# backed by persistent storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"name": "alice",   "role": "admin"},
    2: {"name": "bob",     "role": "moderator"},
    3: {"name": "charlie", "role": "normal"},
}

# Allowed privilege levels
ALLOWED_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_permissions(
    acting_user_id: int,
    targeted_user_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of `targeted_user_id` to
    `new_privilege_level`.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user attempting to perform the change.
    targeted_user_id : int
        The ID of the user whose privilege is to be altered.
    new_privilege_level : str
        The desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # --- Input validation ----------------------------------------------------
    if not isinstance(acting_user_id, int) or not isinstance(targeted_user_id, int):
        return False
    if new_privilege_level not in ALLOWED_PRIVILEGES:
        return False

    # --- Existence checks ----------------------------------------------------
    acting_user = USERS.get(acting_user_id)
    targeted_user = USERS.get(targeted_user_id)

    if acting_user is None or targeted_user is None:
        return False

    # --- Access control ------------------------------------------------------
    # Only admins may modify other users' privileges.
    if acting_user["role"] != "admin":
        return False

    # Optionally prevent admins from demoting themselves
    if acting_user_id == targeted_user_id and new_privilege_level != "admin":
        return False

    # --- Apply change --------------------------------------------------------
    targeted_user["role"] = new_privilege_level
    return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    print(alter_user_permissions(1, 3, "moderator"))  # Expected: True
    print(USERS[3])                                   # Updated role
    print(alter_user_permissions(2, 3, "admin"))      # Expected: False (not admin)