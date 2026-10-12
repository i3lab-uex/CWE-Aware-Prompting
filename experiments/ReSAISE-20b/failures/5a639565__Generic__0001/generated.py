# -*- coding: utf-8 -*-

from __future__ import annotations

from typing import Dict, Set

# Example data structures; in real usage these would be populated elsewhere.
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: {"owner_id": int, "members": set of user_ids}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Allow a project owner or an administrator to add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        ID of the user performing the operation.
    proj_id : int
        ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate operation type
    if operation not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Validate executor role
    executor_role = USERS.get(executor_user_id)
    if executor_role is None:
        return False

    # Only project owners or admins can modify the team
    if executor_role != "admin" and executor_user_id != project["owner_id"]:
        return False

    # Validate target member exists
    if target_member_id not in USERS:
        return False

    members = project["members"]

    if operation == "add":
        # Avoid adding duplicates
        if target_member_id in members:
            return False
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    return True