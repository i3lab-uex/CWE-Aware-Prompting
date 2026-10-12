# -*- coding: utf-8 -*-
"""
Project access management module.

This module defines the `manage_project_access` function, which allows
project owners to add or remove members from their project while admins can
modify any project. The function performs comprehensive authorization checks
to mitigate CWE-862 (Missing Authorization) and related security issues.
"""

from typing import Dict

# Sample data structures – in a real system these would be loaded from a database.
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": set[int]}
}

USERS: Dict[int, str] = {
    # user_id: role ("admin", "owner", "member")
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Modify project membership.

    Parameters
    ----------
    current_user_id : int
        ID of the user invoking the function.
    project_id : int
        Target project ID.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types and values
    if not isinstance(current_user_id, int) or not isinstance(project_id, int) \
       or not isinstance(action, str) or not isinstance(target_user_id, int):
        return False

    if action not in {"add", "remove"}:
        return False

    # Retrieve the current user role
    current_role = USERS.get(current_user_id)
    if current_role is None:
        # Unknown user – deny access
        return False

    # Retrieve project data
    project = PROJECTS.get(project_id)
    if project is None:
        # Unknown project – deny access
        return False

    owner_id = project.get("owner_id")
    members: set[int] = project.get("members", set())

    # Authorization logic
    is_owner = current_user_id == owner_id
    is_admin = current_role.lower() == "admin"

    if not (is_owner or is_admin):
        # Only owners and admins may modify membership
        return False

    # Ensure target user exists in the system
    if USERS.get(target_user_id) is None:
        return False

    # Perform the action
    if action == "add":
        # Prevent duplicate entries; idempotent operation
        members.add(target_user_id)
    else:  # action == "remove"
        # Removing a non-member is harmless but still considered successful
        members.discard(target_user_id)

    # Update the project dictionary (in place)
    project["members"] = members

    return True