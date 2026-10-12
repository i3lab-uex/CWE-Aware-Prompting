# -*- coding: utf-8 -*-
"""
Utility module for managing project team membership with proper access control.
"""

from typing import Dict, List

# Example data structures (in real applications these would be replaced by DB queries)
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    # project_id : {'owner_id': int, 'members': [int]}
}

USERS: Dict[int, str] = {
    # user_id : 'admin' or 'user'
}


def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        ID of the target project.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
            or not isinstance(member_id, int):
        return False

    if operation_type not in {"add", "remove"}:
        return False

    # Verify project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Verify operator exists and has a role
    operator_role = USERS.get(operator_id)
    if not operator_role:
        return False

    # Access control: admins can modify any project
    is_admin = operator_role.lower() == "admin"

    # Non-admins can only modify their own projects
    if not is_admin and operator_id != project["owner_id"]:
        return False

    members = project.get("members", [])
    if operation_type == "add":
        if member_id in members:
            # Already a member; nothing to do
            return True
        members.append(member_id)
    else:  # operation_type == "remove"
        if member_id not in members:
            # Not a member; nothing to do
            return True
        members.remove(member_id)

    # Persist the updated list back into the project record
    project["members"] = members
    return True