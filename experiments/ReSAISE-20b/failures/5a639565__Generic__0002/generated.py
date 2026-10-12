import typing

# Example data structures (replace with real data in production)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {"owner_id": int, "members": set[int]}
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {21, 31}},
}

USERS: dict[int, str] = {
    # user_id: role ("admin" or "user")
    10: "user",
    11: "user",
    20: "user",
    21: "user",
    30: "admin",   # admin user
    31: "user",
}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Allow a project owner or an administrator to add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The ID of the user performing the action.
    proj_id : int
        The project to be modified.
    operation : str
        Either "add" or "remove".
    target_member_id : int
        The user ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation
    if operation not in {"add", "remove"}:
        return False

    project = PROJECTS.get(proj_id)
    if not project:
        # Project does not exist
        return False

    # Verify executor has permission: admin or project owner
    executor_role = USERS.get(executor_user_id)
    if executor_role != "admin" and executor_user_id != project["owner_id"]:
        return False

    members: set[int] = project.get("members", set())

    if operation == "add":
        # Cannot add the owner again
        if target_member_id == project["owner_id"]:
            return False
        # No duplicates
        if target_member_id in members:
            return False
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Prevent removing the owner (not a member but still)
        if target_member_id == project["owner_id"]:
            return False
        members.remove(target_member_id)

    # Update the project's member list
    project["members"] = members
    return True