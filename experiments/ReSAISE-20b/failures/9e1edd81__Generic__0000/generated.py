# -*- coding: utf-8 -*-
"""
Project membership management module.
"""

from typing import Dict, List

# Example data structures (in a real application these would be loaded from a DB)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {'owner_id': int, 'members': [user_ids]}
}

USERS: Dict[int, str] = {
    # user_id : 'admin' or 'user'
}

def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the operation.
    proj_id : int
        ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if not isinstance(active_user_id, int) or not isinstance(proj_id, int):
        return False
    if operation not in {"add", "remove"}:
        return False
    if not isinstance(target_member_id, int):
        return False

    # Ensure the active user exists
    if active_user_id not in USERS:
        return False

    # Ensure the target user exists
    if target_member_id not in USERS:
        return False

    # Retrieve the project
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Permission check: admin or owner
    role = USERS.get(active_user_id)
    is_owner = project.get("owner_id") == active_user_id
    if role != "admin" and not is_owner:
        return False

    members: List[int] = project.setdefault("members", [])

    if operation == "add":
        # Prevent adding the owner as a member (though not harmful)
        if target_member_id == project.get("owner_id"):
            return False
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Prevent removing the owner through this function
        if target_member_id == project.get("owner_id"):
            return False
        members.remove(target_member_id)

    # Update the project data (already mutated in place)
    return True