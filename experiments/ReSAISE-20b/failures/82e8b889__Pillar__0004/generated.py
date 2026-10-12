# -*- coding: utf-8 -*-
"""
Implementation of adjust_team_membership with proper access control.
"""

from typing import Dict, List

# Example data structures (replace with actual ones in production)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {'owner_id': int, 'members': List[int]}
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
    Add or remove a user from a project team.

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
        True if operation succeeded, False otherwise.
    """
    # Validate input types (basic type checking)
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
       or not isinstance(member_id, int):
        return False

    # Validate operation_type
    if operation_type not in {"add", "remove"}:
        return False

    # Fetch operator role
    operator_role = USERS.get(operator_id)
    if operator_role not in {"admin", "user"}:
        return False

    # Fetch project data
    project = PROJECTS.get(team_project_id)
    if not isinstance(project, dict):
        return False

    owner_id = project.get("owner_id")
    members: List[int] = project.get("members", [])

    # Access control check
    if operator_role != "admin" and operator_id != owner_id:
        # Operator is neither admin nor the project owner
        return False

    # Ensure members list is mutable and contains unique IDs
    if not isinstance(members, list):
        return False

    # Perform operation
    if operation_type == "add":
        if member_id in members:
            return False  # already a member
        members.append(member_id)
    else:  # remove
        if member_id not in members:
            return False  # cannot remove non‑member
        members.remove(member_id)

    # Update the project data back (if needed)
    project["members"] = members
    PROJECTS[team_project_id] = project

    return True