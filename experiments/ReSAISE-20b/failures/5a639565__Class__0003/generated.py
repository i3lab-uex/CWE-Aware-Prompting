#!/usr/bin/env python3
"""
Implementation of `manage_team_access` with proper authorization checks.
"""

from typing import Dict, Set

# Example data structures; in real usage these would be imported or injected.
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id : { 'owner_id': int, 'members': set(user_ids) }
}

USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Allows project owners to add/remove members from their projects,
    and administrators to modify any project.

    Parameters
    ----------
    executor_user_id : int
        ID of the user performing the operation.
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
    # Validate input types
    if not isinstance(executor_user_id, int) or not isinstance(proj_id, int) \
       or not isinstance(operation, str) or not isinstance(target_member_id, int):
        return False

    # Normalize operation string
    op = operation.strip().lower()
    if op not in {"add", "remove"}:
        return False

    # Check project existence
    proj = PROJECTS.get(proj_id)
    if not proj:
        return False

    # Check executor role
    executor_role = USERS.get(executor_user_id)
    if executor_role not in {"admin", "user"}:
        return False

    # Authorization: admin can modify any project
    if executor_role == "admin":
        authorized = True
    else:
        # Regular user: must be the owner of the project
        authorized = (proj.get("owner_id") == executor_user_id)

    if not authorized:
        return False

    # Perform the operation
    members: Set[int] = proj.setdefault("members", set())

    if op == "add":
        # Avoid adding duplicates
        members.add(target_member_id)
    else:  # op == "remove"
        members.discard(target_member_id)

    return True