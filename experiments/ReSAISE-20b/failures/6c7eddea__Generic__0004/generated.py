# -*- coding: utf-8 -*-
"""
Utility for modifying user privilege levels.

The module expects a global dictionary `USERS` where each key is an integer
user ID and the value is another dictionary containing at least a `'role'`
key.  The role must be one of the following strings:

* 'normal'
* 'moderator'
* 'admin'

The function `alter_user_privileges` checks that the caller has sufficient
privilege (i.e. is an admin) and that the target user exists.  If all
conditions are met it updates the target's role to `priv_update` and returns
``True``.  Otherwise it returns ``False``.

No database or external dependencies are used; this is a pure‑Python example
that can be adapted to real persistence layers.
"""

from typing import Dict

# Example user store.  In a production system this would be backed by a
# database or other persistent storage.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "moderator"},
    3: {"role": "normal"},
}

# Valid privilege levels.
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int,
                          priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the administrator attempting the change.
    tar_user_id : int
        ID of the user whose privileges will be changed.
    priv_update : str
        New privilege level to assign.

    Returns
    -------
    bool
        ``True`` if the change succeeded, otherwise ``False``.

    Notes
    -----
    * Only users with role ``admin`` are allowed to change other users'
      privileges.
    * The function silently returns ``False`` if the target user does not
      exist or if the requested privilege level is invalid.
    * The caller cannot demote themselves; attempts to change their own
      role are rejected.
    """
    # Validate target privilege level.
    if priv_update not in VALID_PRIVILEGES:
        return False

    # Ensure the current user exists.
    cur_user = USERS.get(cur_user_id)
    if not cur_user:
        return False

    # Ensure the target user exists.
    tar_user = USERS.get(tar_user_id)
    if not tar_user:
        return False

    # Prevent self‑modification of privileges.
    if cur_user_id == tar_user_id:
        return False

    # Only admins can modify privileges.
    if cur_user.get("role") != "admin":
        return False

    # Perform the update.
    tar_user["role"] = priv_update
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(alter_user_privileges(1, 3, "moderator"))  # Expected: True
    print(USERS[3]["role"])                          # Expected: "moderator"