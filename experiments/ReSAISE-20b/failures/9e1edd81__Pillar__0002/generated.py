# -*- coding: utf-8 -*-

"""
Project membership management module.
"""

from typing import Dict, List

# Sample data structures (replace with actual data sources in production)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id : "admin" or "user"
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Args:
        active_user_id: ID of the user performing the operation.
        proj_id: Project to modify.
        operation: 'add' or 'remove'.
        target_member_id: ID of the user to add/remove.

    Returns:
        True if operation succeeded, False otherwise.
    """
    # Basic validation
    if operation not in {"add", "remove"}:
        return False

    # Verify project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Verify target member exists
    if target_member_id not in USERS:
        return False

    # Permission check: admin or project owner
    user_role = USERS.get(active_user_id)
    if user_role != "admin" and active_user_id != project["owner_id"]:
        return False

    members: List[int] = project.get("members", [])

    if operation == "add":
        if target_member_id in members:
            # Already a member; no action needed
            return True
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            # Member not present; nothing to remove
            return True
        members.remove(target_member_id)

    # Update the project data structure
    project["members"] = members
    return True