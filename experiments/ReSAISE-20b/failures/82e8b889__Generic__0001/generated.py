import typing

# Sample data structures (replace with actual application state)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}
USERS: dict[int, str] = {
    # user_id: "admin" or "user"
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
        ID of the user performing the operation.
    team_project_id : int
        ID of the project to modify.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate operation type early
    if operation_type not in {"add", "remove"}:
        raise ValueError("operation_type must be 'add' or 'remove'")

    # Check that the project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Permission check: owner or admin
    operator_role = USERS.get(operator_id)
    if operator_role != "admin" and operator_id != project["owner_id"]:
        return False

    members = project.setdefault("members", [])

    if operation_type == "add":
        # Prevent duplicates
        if member_id in members:
            return False
        members.append(member_id)
    else:  # remove
        if member_id not in members:
            return False
        members.remove(member_id)

    return True