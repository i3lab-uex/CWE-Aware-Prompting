# -*- coding: utf-8 -*-
"""
Utility for adjusting project team membership with proper access control.
"""

from typing import Dict, List

# Example data structures (replace with actual storage in production)
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" | "user"
}


def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int,
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        The ID of the user performing the operation.
    team_project_id : int
        The project to be modified.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        The user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
       or not isinstance(member_id, int):
        return False

    if operation_type not in {"add", "remove"}:
        return False

    # Retrieve project
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Retrieve operator role
    operator_role = USERS.get(operator_id)
    if not operator_role:
        return False

    # Access control: admin or owner
    is_owner = project.get("owner_id") == operator_id
    if operator_role != "admin" and not is_owner:
        return False

    members: List[int] = project.get("members", [])
    if operation_type == "add":
        # Prevent duplicate addition
        if member_id in members:
            return False
        members.append(member_id)
    else:  # remove
        if member_id not in members:
            return False
        members.remove(member_id)

    # Persist changes back to the data store (here we just update the dict)
    project["members"] = members
    return True