# -------------------------------------------------------------
# User privilege management module
# -------------------------------------------------------------

from typing import Dict

# Example user store: mapping user_id -> {"role": str, "privilege": str}
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin",     "privilege": "admin"},
    2: {"role": "moderator", "privilege": "moderator"},
    3: {"role": "user",      "privilege": "normal"},
    # ... other users ...
}

# Valid privilege levels
VALID_PRIVILEGES = {"normal", "moderator", "admin"}


def alter_user_privileges(cur_user_id: int, tar_user_id: int, priv_update: str) -> bool:
    """
    Change the privilege level of a target user.

    Parameters
    ----------
    cur_user_id : int
        ID of the administrator attempting to make the change.
    tar_user_id : int
        ID of the user whose privilege level is to be updated.
    priv_update : str
        New privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege change succeeded, False otherwise.
    """
    # 1. Validate existence of current user
    cur_user = USERS.get(cur_user_id)
    if not cur_user:
        # Current user does not exist
        return False

    # 2. Only admins may change privileges
    if cur_user["privilege"] != "admin":
        return False

    # 3. Validate target user exists
    tar_user = USERS.get(tar_user_id)
    if not tar_user:
        return False

    # 4. Validate new privilege level
    priv_update = priv_update.lower()
    if priv_update not in VALID_PRIVILEGES:
        return False

    # 5. Prevent self‑downgrading of admin privileges
    if cur_user_id == tar_user_id and priv_update != "admin":
        # Admin cannot lower their own privilege level
        return False

    # 6. Apply the change atomically (dictionary assignment is atomic for CPython)
    USERS[tar_user_id]["privilege"] = priv_update

    return True