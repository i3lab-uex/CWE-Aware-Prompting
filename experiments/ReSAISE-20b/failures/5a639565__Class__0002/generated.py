from __future__ import annotations

# Sample data structures; in real use these would come from a database or config
PROJECTS = {
    # project_id: {"owner_id": int, "members": set[int]}
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {40}},
}

USERS = {
    # user_id: {"role": str}
    10: {"role": "user"},
    11: {"role": "user"},
    12: {"role": "admin"},   # administrator
}

def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The ID of the user performing the action.
    proj_id : int
        The project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user ID to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if operation not in {"add", "remove"}:
        return False

    # Verify that the project exists
    proj = PROJECTS.get(proj_id)
    if not proj:
        return False

    # Verify that the executor exists
    executor = USERS.get(executor_user_id)
    if not executor:
        return False

    # Verify that the target member exists
    if target_member_id not in USERS:
        return False

    # Authorization: admin can modify any project
    if executor["role"] == "admin":
        authorized = True
    else:
        # Non-admins can only modify their own projects
        authorized = executor_user_id == proj["owner_id"]

    if not authorized:
        return False

    # Perform the operation
    members = proj["members"]
    if operation == "add":
        members.add(target_member_id)
    else:  # remove
        if target_member_id in members:
            members.remove(target_member_id)
        else:
            # Trying to remove a non‑member is considered a failure
            return False

    return True