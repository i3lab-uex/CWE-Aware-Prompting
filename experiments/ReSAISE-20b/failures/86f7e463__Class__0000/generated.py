#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Project membership management module.
"""

from typing import Dict, List

# Sample data structures (replace with real database lookups in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [user_ids]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation of inputs
    if modification not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Verify that the user performing the action exists
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Authorization: allow only project owner or admins
    if acting_user_id != project["owner_id"] and acting_role.lower() != "admin":
        return False

    # Verify that the target user exists
    if user_to_update_id not in USERS:
        return False

    members = project.setdefault("members", [])

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # In a real system, persist changes to the database here

    return True