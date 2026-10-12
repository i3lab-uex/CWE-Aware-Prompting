# -*- coding: utf-8 -*-
"""
Utility module for project membership management.
"""

from typing import Dict, List

# Sample data structures (replace with actual application data)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : { 'owner_id': int, 'members': [int, ...] }
    1: {"owner_id": 101, "members": [102, 103]},
    2: {"owner_id": 104, "members": []},
}

USERS: Dict[int, str] = {
    # user_id : role ('user' or 'admin')
    101: "user",
    102: "user",
    103: "admin",
    104: "user",
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the operation.
    proj_id : int
        ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.

    Notes
    -----
    - Only the project owner or a user with role 'admin' can modify membership.
    - The function performs all necessary authorization checks to mitigate
      CWE-862 (Missing Authorization).
    """
    # Basic validation of input parameters
    if operation not in {"add", "remove"}:
        raise ValueError("operation must be 'add' or 'remove'")

    # Verify that the active user exists
    if active_user_id not in USERS:
        return False

    # Verify that the target user exists
    if target_member_id not in USERS:
        return False

    # Retrieve the project data; fail gracefully if missing
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Authorization: owner or admin
    is_owner = project["owner_id"] == active_user_id
    is_admin = USERS.get(active_user_id) == "admin"
    if not (is_owner or is_admin):
        return False

    members = project.setdefault("members", [])

    if operation == "add":
        # Avoid duplicate membership
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Optionally, persist changes here (e.g., database commit)
    return True