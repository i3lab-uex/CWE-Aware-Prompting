# -*- coding: utf-8 -*-
"""
Project team access manager.

The module defines a single public function `manage_team_access` that allows
project owners to add or remove members from their own projects.  System
administrators may perform the same operation on any project.

The data model is simplified for demonstration purposes: two global dictionaries
`PROJECTS` and `USERS` are expected to be defined elsewhere in the application.
"""

from typing import Dict, Set

# Example data structures (replace with real ones in production)
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: {"owner_id": int, "members": set of user_ids}
}

USERS: Dict[int, Set[str]] = {
    # user_id: {"role1", "role2", ...}
}


def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return "admin" in USERS.get(user_id, set())


def _is_owner(project: Dict[str, Set[int]], user_id: int) -> bool:
    """Return True if the user is the owner of the project."""
    return project.get("owner_id") == user_id


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Modify the membership of a project.

    Parameters
    ----------
    executor_user_id : int
        The user performing the operation.
    proj_id : int
        Identifier of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        User ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Validate executor existence
    if executor_user_id not in USERS:
        return False

    # Permission check: admin or owner
    if not (_is_admin(executor_user_id) or _is_owner(project, executor_user_id)):
        return False

    # Validate target member existence
    if target_member_id not in USERS:
        return False

    members = project.setdefault("members", set())

    if operation == "add":
        # Avoid duplicate addition
        if target_member_id in members:
            return False
        members.add(target_member_id)
    elif operation == "remove":
        if target_member_id not in members:
            return False
        members.remove(target_member_id)
    else:
        # Unsupported operation string
        return False

    return True