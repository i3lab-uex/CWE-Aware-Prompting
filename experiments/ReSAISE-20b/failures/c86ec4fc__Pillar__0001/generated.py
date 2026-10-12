# -*- coding: utf-8 -*-
"""
Module providing a function to control project participants with proper access checks.
"""

from typing import Dict, Set

# Sample data structures (replace with actual database lookups in production)
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: {"owner_id": int, "members": set of user_ids}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Allows a project owner or an administrator to add or remove members from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate existence of acting user and target user
    if acting_user_id not in USERS or target_id not in USERS:
        return False

    # Validate project existence
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    owner_id: int = project.get("owner_id")
    members: Set[int] = project.get("members", set())

    # Determine if acting user has permission
    is_admin: bool = USERS[acting_user_id] == "admin"
    is_owner: bool = acting_user_id == owner_id

    if not (is_admin or is_owner):
        # Unauthorized user
        return False

    action = action_type.lower()
    if action == "add":
        # Cannot add the owner again
        if target_id == owner_id:
            return False
        # Avoid duplicate addition
        if target_id in members:
            return False
        members.add(target_id)
    elif action == "remove":
        # Owner cannot be removed by non-admin
        if target_id == owner_id and not is_admin:
            return False
        # If target is not a member, nothing to do
        if target_id not in members:
            return False
        members.remove(target_id)
    else:
        # Invalid action_type
        return False

    # Update the project's member set (in case of immutable types)
    PROJECTS[prj_id]["members"] = members
    return True