# -*- coding: utf-8 -*-

"""
Utility module for user privilege management.

The global `USERS` dictionary is expected to have the following structure:
{
    user_id: {
        "username": str,
        "role": str,          # one of 'normal', 'moderator', 'admin'
        ...
    },
    ...
}
"""

from typing import Dict

# Example USERS dictionary (in practice this would come from a database or external source)
USERS: Dict[int, dict] = {
    1: {"username": "alice", "role": "admin"},
    2: {"username": "bob",   "role": "moderator"},
    3: {"username": "carol", "role": "normal"},
}


def change_user_role(
    modifying_user_id: int,
    user_to_change_id: int,
    new_privilege_level: str
) -> bool:
    """
    Change the privilege level of a user.

    Parameters
    ----------
    modifying_user_id : int
        The ID of the user attempting to perform the change.
    user_to_change_id : int
        The ID of the user whose privilege is being altered.
    new_privilege_level : str
        Desired new privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the change succeeded, False otherwise.
    """
    # Validate privilege levels
    valid_levels = {"normal", "moderator", "admin"}
    if new_privilege_level not in valid_levels:
        return False

    # Retrieve user records
    modifier = USERS.get(modifying_user_id)
    target   = USERS.get(user_to_change_id)

    # Basic existence checks
    if modifier is None or target is None:
        return False

    # Only admins may modify other users' privileges
    if modifier.get("role") != "admin":
        return False

    # Prevent self‑downgrading to a lower privilege than current
    if modifying_user_id == user_to_change_id:
        # Admin cannot demote themselves to a lower level
        if valid_levels.index(new_privilege_level) < valid_levels.index(modifier.get("role")):
            return False

    # Apply the change
    target["role"] = new_privilege_level
    return True


# Example usage (uncomment to test)
if __name__ == "__main__":
    print(change_user_role(1, 3, "moderator"))  # True
    print(USERS[3]["role"])                    # 'moderator'