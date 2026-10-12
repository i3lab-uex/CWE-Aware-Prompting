import typing

# Sample data structures (replace with actual ones in production)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {"owner_id": int, "members": set[int]}
}

USERS: dict[int, str] = {
    # user_id: "role"  (e.g., "admin", "user")
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The user invoking the function.
    project_id : int
        Identifier of the target project.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If `action` is not 'add' or 'remove'.
    KeyError
        If the project, current user, or target user does not exist.
    """
    # Validate action
    if action not in {"add", "remove"}:
        raise ValueError("action must be 'add' or 'remove'")

    # Fetch project, current user role, and target existence
    try:
        project = PROJECTS[project_id]
    except KeyError as exc:
        raise KeyError(f"Project {project_id} not found") from exc

    try:
        current_role = USERS[current_user_id]
    except KeyError as exc:
        raise KeyError(f"User {current_user_id} not found") from exc

    if target_user_id not in USERS:
        raise KeyError(f"Target user {target_user_id} not found")

    # Authorization check: admins can modify any project,
    # owners can modify their own projects
    if not (current_role == "admin" or current_user_id == project["owner_id"]):
        return False

    members = project.setdefault("members", set())

    if action == "add":
        members.add(target_user_id)
    else:  # action == "remove"
        members.discard(target_user_id)

    return True