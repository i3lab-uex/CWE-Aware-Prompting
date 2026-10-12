# -*- coding: utf-8 -*-

"""
Project access control module.

This module provides the `project_access_control` function which enforces
proper authorization when adding or removing members from a project.
"""

from typing import Dict, List

# Example data structures. In real use these would be populated from a database.
PROJECTS: Dict[int, Dict] = {
    # project_id: { "owner_id": int, "members": List[int] }
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int,
) -> bool:
    """
    Add or remove a member from a project if the active user is authorized.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project identifier.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        User ID of the member to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Verify that the active user exists and has a role
    active_role = USERS.get(active_user_id)
    if active_role is None:
        return False

    # Verify that the target member exists
    if member_user_id not in USERS:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Determine authorization
    is_admin = active_role == "admin"
    is_owner = project.get("owner_id") == active_user_id

    if not (is_admin or is_owner):
        return False  # Unauthorized

    members: List[int] = project.setdefault("members", [])

    if action_type == "add":
        # Avoid duplicates
        if member_user_id in members:
            return False  # Already a member
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False  # Not a current member
        members.remove(member_user_id)

    return True