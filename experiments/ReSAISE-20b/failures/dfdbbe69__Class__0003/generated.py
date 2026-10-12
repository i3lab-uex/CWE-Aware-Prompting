# -*- coding: utf-8 -*-
"""
Project membership management module.

This module provides a single function `handle_project_membership` that allows
project owners to add or remove members from their own projects, and lets
administrators modify any project.  It performs comprehensive validation of
input arguments and enforces role‑based access control to mitigate the risk
of CWE-862 (Missing Authorization).

Author: ChatGPT
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Example data structures.  In a real system these would be replaced by
# database lookups or ORM queries.
# --------------------------------------------------------------------------- #
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : { 'role': 'admin' | 'user', ... }
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
    4: {"role": "user"},
}

PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id : { 'owner_id': int, 'members': set[int], ... }
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #
def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the action.
    proj_id : int
        Target project ID.
    mod : str
        Operation to perform: either 'add' or 'remove'.
    mod_user_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Notes
    -----
    * Only project owners and administrators may modify membership.
    * The function validates that all user IDs exist, the project exists,
      and the operation is well‑formed.
    * It returns False on any failure instead of raising exceptions,
      to keep the API simple for callers that only need a success flag.
    """

    # --------------------------------------------------------------------- #
    # Basic sanity checks
    # --------------------------------------------------------------------- #
    if not isinstance(req_user_id, int) or not isinstance(proj_id, int):
        return False
    if mod not in {"add", "remove"}:
        return False

    # Ensure the requestor exists
    requester = USERS.get(req_user_id)
    if not requester:
        return False

    # Ensure the target project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure the target user exists
    target_user = USERS.get(mod_user_id)
    if not target_user:
        return False

    # --------------------------------------------------------------------- #
    # Authorization: allow if requester is an admin or the project owner
    # --------------------------------------------------------------------- #
    is_admin = requester.get("role") == "admin"
    is_owner = project.get("owner_id") == req_user_id

    if not (is_admin or is_owner):
        return False

    # --------------------------------------------------------------------- #
    # Perform the requested modification
    # --------------------------------------------------------------------- #
    members: set[int] = project.setdefault("members", set())

    if mod == "add":
        members.add(mod_user_id)
    else:  # mod == "remove"
        members.discard(mod_user_id)

    return True

# --------------------------------------------------------------------------- #
# Example usage
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    # Owner adding a user
    print(handle_project_membership(2, 101, "add", 4))   # True

    # Non‑owner attempting to add
    print(handle_project_membership(3, 101, "add", 4))   # False

    # Admin removing a user
    print(handle_project_membership(1, 102, "remove", 3)) # True