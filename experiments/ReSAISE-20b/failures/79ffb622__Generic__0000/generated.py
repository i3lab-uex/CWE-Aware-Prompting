# -*- coding: utf-8 -*-
"""
Utility for managing user privileges in a simple in‑memory store.
"""

from typing import Dict

# Example USERS dictionary. In real usage this would be loaded from a DB or
# persistent store. The structure is:
#
#   USERS = {
#       user_id: {
#           "name": str,
#           "role": str,          # 'normal', 'moderator', or 'admin'
#           "privilege": str,     # same set as role
#       },
#       ...
#   }
#
USERS: Dict[int, Dict[str, str]] = {}


def change_user_privileges(
    requesting_user_id: int,
    user_to_change_id: int,
    desired_privilege: str
) -> bool:
    """
    Allows an admin user to change the privilege level of another user.

    Parameters
    ----------
    requesting_user_id : int
        The ID of the user making the request.
    user_to_change_id : int
        The ID of the target user whose privilege will be changed.
    desired_privilege : str
        Desired privilege level ('normal', 'moderator', or 'admin').

    Returns
    -------
    bool
        True if the privilege was changed successfully, False otherwise.
    """
    # ------------------------------------------------------------------
    # 1. Validate input privilege
    # ------------------------------------------------------------------
    VALID_PRIVILEGES = {"normal", "moderator", "admin"}
    if desired_privilege not in VALID_PRIVILEGES:
        return False

    # ------------------------------------------------------------------
    # 2. Fetch users from the store
    # ------------------------------------------------------------------
    requester = USERS.get(requesting_user_id)
    target = USERS.get(user_to_change_id)

    if requester is None or target is None:
        # Either the requesting user or target does not exist
        return False

    # ------------------------------------------------------------------
    # 3. Ensure the requester has admin rights
    # ------------------------------------------------------------------
    if requester.get("role") != "admin":
        return False

    # ------------------------------------------------------------------
    # 4. Prevent an admin from demoting themselves
    # ------------------------------------------------------------------
    if requesting_user_id == user_to_change_id and desired_privilege != "admin":
        return False

    # ------------------------------------------------------------------
    # 5. Apply the privilege change
    # ------------------------------------------------------------------
    try:
        target["privilege"] = desired_privilege
        # Optionally keep the role in sync with privilege if you consider them equivalent.
        target["role"] = desired_privilege
    except Exception:
        # Any unforeseen error (e.g., read‑only dict) results in failure.
        return False

    return True