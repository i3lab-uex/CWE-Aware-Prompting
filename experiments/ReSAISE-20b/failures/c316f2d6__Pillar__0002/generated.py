# -*- coding: utf-8 -*-
"""
Implementation of a project access management function.
"""

from typing import Dict, Any

# Example data structures. In real usage these would be imported from
# the application's data layer.
PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id : {'owner_id': int, 'members': set[int]}
}
USERS: Dict[int, str] = {
    # user_id : role (e.g., 'admin', 'user')
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
        The ID of the user performing the operation.
    project_id : int
        The ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action type
    if action not in {"add", "remove"}:
        raise ValueError("action must be 'add' or 'remove'")

    # Retrieve project data
    project = PROJECTS.get(project_id)
    if not project:
        return False  # Project does not exist

    owner_id = project.get("owner_id")
    members: set[int] = project.setdefault("members", set())

    # Retrieve user role
    current_role = USERS.get(current_user_id)
    if not current_role:
        return False  # Unknown user

    # Permission check: admins can modify any project; owners can modify only their own
    if current_role != "admin" and current_user_id != owner_id:
        return False  # Not authorized

    if action == "add":
        # Avoid adding duplicates
        if target_user_id in members:
            return False  # Already a member
        members.add(target_user_id)
    else:  # action == "remove"
        if target_user_id not in members:
            return False  # Not a member
        members.remove(target_user_id)

    return True