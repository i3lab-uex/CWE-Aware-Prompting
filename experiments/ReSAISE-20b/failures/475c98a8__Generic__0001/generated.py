# -*- coding: utf-8 -*-
"""
Utility module for managing user privileges.
"""

from typing import Dict

# Example USERS dictionary. In a real application this would be loaded from
# persistent storage (e.g., database). The keys are user IDs and the values
# are dictionaries containing a 'role' key.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
    # ... more users
}

# Valid privilege levels that can be assigned.
VALID_ROLES = {"normal", "moderator", "admin"}


def update_user_roles(curr_user_id: int, targ_user_id: int, privilege_change: str) -> bool:
    """
    Update the role of a target user if the current user is an admin.

    Parameters
    ----------
    curr_user_id : int
        ID of the user attempting to perform the update.
    targ_user_id : int
        ID of the target user whose role is to be changed.
    privilege_change : str
        New role to assign. Must be one of 'normal', 'moderator', or 'admin'.

    Returns
    -------
    bool
        True if the update succeeded, False otherwise.

    Notes
    -----
    * The current user must exist and have the 'admin' role.
    * The target user must exist in the USERS dictionary.
    * The new privilege level must be one of VALID_ROLES.
    """
    # Quick sanity checks
    if not isinstance(curr_user_id, int) or not isinstance(targ_user_id, int):
        return False
    if privilege_change not in VALID_ROLES:
        return False

    # Ensure both users exist
    curr_user = USERS.get(curr_user_id)
    targ_user = USERS.get(targ_user_id)

    if curr_user is None or targ_user is None:
        return False

    # Verify current user has admin rights
    if curr_user.get("role") != "admin":
        return False

    # Perform the role update
    targ_user["role"] = privilege_change
    return True


# Example usage (for testing only; remove or guard under __main__ in production)
if __name__ == "__main__":
    print(update_user_roles(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                      # Expected: "moderator"