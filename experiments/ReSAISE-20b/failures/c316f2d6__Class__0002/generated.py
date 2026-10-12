from typing import Dict

# Sample data structures (these would normally come from a database or config)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {'owner_id': int, 'members': set of user_ids}
}

USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
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
        The ID of the user performing the action.
    project_id : int
        The ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The ID of the user to add or remove from the project.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if action not in {"add", "remove"}:
        raise ValueError("action must be 'add' or 'remove'")
    if current_user_id not in USERS:
        return False
    if target_user_id not in USERS:
        return False
    if project_id not in PROJECTS:
        return False

    # Authorization: only the owner or an admin can modify the project
    owner_id = PROJECTS[project_id]["owner_id"]
    if current_user_id != owner_id and USERS[current_user_id] != "admin":
        return False

    members = PROJECTS[project_id]["members"]
    if action == "add":
        # Adding an existing member is a no-op but considered success
        members.add(target_user_id)
    else:  # action == "remove"
        # Removing a non‑member is also considered success (idempotent)
        members.discard(target_user_id)

    return True