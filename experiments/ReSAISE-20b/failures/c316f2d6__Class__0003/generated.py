# -*- coding: utf-8 -*-
"""
Implementation of project access management with proper authorization checks.
"""

from typing import Dict, Set

# Sample data structures (these would normally be populated elsewhere)
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: {'owner_id': int, 'members': set of user_ids}
}

USERS: Dict[int, str] = {
    # user_id: role ('admin', 'owner', 'member')
}

def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The user performing the operation.
    project_id : int
        Identifier of the target project.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input parameters
    if action not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Verify that the target user exists
    if target_user_id not in USERS:
        return False

    # Authorization: allow admins or the project owner to modify
    current_role = USERS.get(current_user_id)
    if current_role != "admin" and current_user_id != project["owner_id"]:
        return False

    members: Set[int] = project.get("members", set())

    if action == "add":
        # Prevent adding the owner as a member (optional rule)
        if target_user_id == project["owner_id"]:
            return False
        # Avoid duplicate additions
        if target_user_id in members:
            return True  # Already a member; consider success
        members.add(target_user_id)
    else:  # action == "remove"
        if target_user_id not in members:
            return True  # Already removed; consider success
        members.remove(target_user_id)

    # Persist changes back to the project dict
    project["members"] = members
    return True