# -*- coding: utf-8 -*-

"""
Project access management module.
"""

from typing import Dict, Any

# Example data structures (replace with real data sources in production)
PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id : {'owner_id': int, 'members': set[int]}
}

USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {'role': str}
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Allows a project owner to add or remove members from their project.
    Admins can modify any project.

    Parameters
    ----------
    current_user_id : int
        The user ID of the actor invoking the function.
    project_id : int
        The ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user ID of the member being added or removed.

    Returns
    -------
    bool
        True if the action succeeded, False otherwise.
    """

    # Basic validation of input arguments
    if action not in {"add", "remove"}:
        return False

    # Verify the project exists
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Verify the target user exists
    if target_user_id not in USERS:
        return False

    # Determine the role of the current user
    current_user = USERS.get(current_user_id)
    if not current_user:
        return False

    role = current_user.get("role")
    # Admins can modify any project
    is_admin = role == "admin"

    # Owners can modify only their own projects
    is_owner = project.get("owner_id") == current_user_id

    if not (is_admin or is_owner):
        # Unauthorized attempt
        return False

    members = project.setdefault("members", set())

    if action == "add":
        # Avoid adding the owner as a member (owner is implicit)
        if target_user_id == project.get("owner_id"):
            return False
        members.add(target_user_id)
    else:  # action == "remove"
        # Prevent removing the owner
        if target_user_id == project.get("owner_id"):
            return False
        members.discard(target_user_id)

    # Persist changes (in real implementation this would write to a database)
    PROJECTS[project_id]["members"] = members

    return True