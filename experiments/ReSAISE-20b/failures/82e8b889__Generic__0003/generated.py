# Adjust team membership for projects with role-based access control

from typing import Dict, List

# Example data structures (should be defined elsewhere in the application)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {'owner_id': int, 'members': [int]}
}

USERS: Dict[int, str] = {
    # user_id: 'admin' or 'user'
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
        ID of the project to modify.
    operation_type : str
        'add' or 'remove'.
    member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if operation_type not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Verify that the operator exists and determine role
    operator_role = USERS.get(operator_id)
    if not operator_role:
        return False

    # Only admins or the project owner can modify membership
    if operator_role != "admin" and operator_id != project["owner_id"]:
        return False

    # Ensure member exists in USERS (optional but prevents orphan entries)
    if member_id not in USERS:
        return False

    members = project.setdefault("members", [])

    if operation_type == "add":
        # Prevent adding duplicate members
        if member_id in members:
            return False
        members.append(member_id)
    else:  # operation_type == "remove"
        if member_id not in members:
            return False
        members.remove(member_id)

    # If we reach here, the operation succeeded
    return True