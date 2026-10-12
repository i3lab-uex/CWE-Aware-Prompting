# -*- coding: utf-8 -*-

from typing import Dict

# Sample data structures (replace with actual application data)
PROJECTS: Dict[int, Dict[str, any]] = {
    # Example: project_id -> {'owner_id': int, 'members': set[int]}
    1: {'owner_id': 10, 'members': {20, 30}},
    2: {'owner_id': 11, 'members': {31}}
}

USERS: Dict[int, str] = {
    # Example: user_id -> role ('admin' or 'user')
    10: 'admin',
    11: 'user',
    20: 'user',
    30: 'user',
    31: 'user'
}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Allow a project owner to add or remove members from their own project.
    Administrators may modify any project.

    Parameters
    ----------
    executor_user_id : int
        ID of the user performing the action.
    proj_id : int
        Target project ID.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the member to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if not isinstance(executor_user_id, int) or not isinstance(proj_id, int):
        return False
    if operation not in {"add", "remove"}:
        return False
    if not isinstance(target_member_id, int):
        return False

    # Check project existence
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Fetch executor role; default to 'user' if unknown
    executor_role = USERS.get(executor_user_id, "user")

    # Authorization: admin can modify any project
    if executor_role == "admin":
        authorized = True
    else:
        # Non-admin must be the owner of the project
        authorized = executor_user_id == project.get("owner_id")

    if not authorized:
        return False

    members = project.setdefault("members", set())

    # Perform the requested operation
    if operation == "add":
        members.add(target_member_id)
    else:  # remove
        members.discard(target_member_id)

    return True