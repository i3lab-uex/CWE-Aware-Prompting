# -*- coding: utf-8 -*-

from typing import Dict, List

# Example data structures. In a real application these would be replaced
# with database queries or ORM models.
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    # project_id : { 'owner_id': int, 'members': [int] }
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
    Adds or removes a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        ID of the project to modify.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """

    # Basic input validation
    if operation_type not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Authorization check: operator must be the owner or an admin
    operator_role = USERS.get(operator_id)
    if operator_role != "admin" and project["owner_id"] != operator_id:
        return False

    members: List[int] = project.get("members", [])

    if operation_type == "add":
        # Avoid duplicate entries
        if member_id in members:
            return False
        members.append(member_id)
    else:  # operation_type == "remove"
        if member_id not in members:
            return False
        members.remove(member_id)

    # Update the project's member list
    project["members"] = members
    return True