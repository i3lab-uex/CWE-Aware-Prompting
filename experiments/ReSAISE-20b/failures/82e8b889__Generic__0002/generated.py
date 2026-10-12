from typing import Dict, List

# Example data structures (replace with actual ones in your application)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
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
        True if operation succeeded, False otherwise.
    """
    # Basic validation of input types and values
    if not isinstance(operator_id, int) or not isinstance(team_project_id, int) \
       or not isinstance(member_id, int):
        return False

    if operation_type not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Verify that the member exists
    if member_id not in USERS:
        return False

    # Determine permission: operator must be project owner or an admin
    if USERS.get(operator_id) != "admin" and operator_id != project["owner_id"]:
        return False

    members: List[int] = project.get("members", [])

    if operation_type == "add":
        # Prevent duplicate additions
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