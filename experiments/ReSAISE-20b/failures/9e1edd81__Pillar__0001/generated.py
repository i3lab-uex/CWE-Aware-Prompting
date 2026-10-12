# -*- coding: utf-8 -*-
"""
Utility module for project membership management.
"""

from typing import Dict, List

# Example data structures (replace with actual storage in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}
USERS: Dict[int, str] = {
    # user_id: "admin" | "user"
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project, respecting ownership and admin privileges.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the operation.
    proj_id : int
        The ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(active_user_id, int) or not isinstance(proj_id, int) \
       or not isinstance(target_member_id, int):
        return False

    if operation not in {"add", "remove"}:
        return False

    # Ensure the active user exists
    active_role = USERS.get(active_user_id)
    if active_role is None:
        return False

    # Ensure the target user exists
    if target_member_id not in USERS:
        return False

    # Ensure the project exists
    proj = PROJECTS.get(proj_id)
    if proj is None:
        return False

    # Permission check: admin can do anything; owner can modify their own project
    if active_role != "admin" and proj.get("owner_id") != active_user_id:
        return False

    members = proj.setdefault("members", [])

    if operation == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Optional: persist changes to storage if using a database
    return True