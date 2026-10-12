import typing

# Example data structures (replace with real ones in your application)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {'owner_id': int, 'members': set[int]}
}

USERS: dict[int, dict[str, typing.Any]] = {
    # user_id: {'role': str}
}

def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Allows project owners to add or remove members from their project,
    while admins can modify any project.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor invoking the function.
    project_id : int
        The ID of the project being modified.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user ID of the member being added or removed.

    Returns
    -------
    bool
        True if the action was successfully performed, otherwise False.
    """
    # Basic validation of input types
    if not isinstance(action, str) or action.lower() not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Ensure the target user exists
    if target_user_id not in USERS:
        return False

    # Check permissions: admin or owner
    current_user = USERS.get(current_user_id)
    if not current_user:
        return False

    is_admin = current_user.get("role") == "admin"
    is_owner = project.get("owner_id") == current_user_id

    if not (is_admin or is_owner):
        return False

    members = project.setdefault("members", set())

    # Perform the action
    if action.lower() == "add":
        members.add(target_user_id)
    else:  # remove
        members.discard(target_user_id)

    return True