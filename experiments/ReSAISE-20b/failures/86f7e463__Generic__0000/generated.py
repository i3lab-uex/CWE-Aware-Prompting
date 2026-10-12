import typing

# Example data structures (replace with actual application data)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {"owner_id": int, "members": [int]}
}
USERS: dict[int, str] = {
    # user_id: "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if modification not in {"add", "remove"}:
        return False

    # Verify that both users exist
    if acting_user_id not in USERS or user_to_update_id not in USERS:
        return False

    # Verify project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    owner_id: int = project.get("owner_id")
    members: list[int] = project.get("members", [])

    # Permission check: acting user must be owner or admin
    if acting_user_id != owner_id and USERS.get(acting_user_id) != "admin":
        return False

    # Prevent removing the owner from members
    if modification == "remove" and user_to_update_id == owner_id:
        return False

    if modification == "add":
        if user_to_update_id in members or user_to_update_id == owner_id:
            return False
        members.append(user_to_update_id)
    else:  # remove
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Update the project data structure
    project["members"] = members
    return True