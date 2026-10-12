# adjust_team_membership.py

from typing import Dict, List

# Example data structures (in real use these would be persisted in a DB)
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    # project_id: {'owner_id': int, 'members': [user_ids]}
}

USERS: Dict[int, str] = {
    # user_id: role ('user' or 'admin')
}


def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Args:
        operator_id (int): ID of the user performing the operation.
        team_project_id (int): Project to modify.
        operation_type (str): 'add' or 'remove'.
        member_id (int): User to add/remove.

    Returns:
        bool: True if operation succeeded, False otherwise.
    """
    # Basic input validation
    if operation_type not in {"add", "remove"}:
        return False

    # Check that operator exists
    if operator_id not in USERS:
        return False

    # Retrieve project info
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Authorization: admin can do anything; otherwise only owner
    operator_role = USERS.get(operator_id)
    if operator_role != "admin" and project["owner_id"] != operator_id:
        return False

    # Ensure member exists
    if member_id not in USERS:
        return False

    members: List[int] = project.get("members", [])

    if operation_type == "add":
        if member_id in members:
            return False  # already a member
        members.append(member_id)
    else:  # remove
        if member_id not in members:
            return False  # not a member
        members.remove(member_id)

    # Update project data
    project["members"] = members
    return True