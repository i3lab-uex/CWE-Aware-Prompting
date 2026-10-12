# -*- coding: utf-8 -*-

"""
Utility for managing project membership.

The module assumes the presence of two global dictionaries:
    PROJECTS: Mapping from project_id to a dict with keys
              'owner_id' (int) and 'members' (list[int]).
    USERS:   Mapping from user_id to a dict with key
              'role' (str) – either 'user' or 'admin'.
"""

from typing import Dict, List

# Example global data structures (to be replaced by actual data in the application)
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {}
USERS: Dict[int, Dict[str, str]] = {}


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
        ID of the member to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate modification keyword
    if modification not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Ensure the acting user exists
    acting_user = USERS.get(acting_user_id)
    if not acting_user:
        return False

    # Check permission: owner or admin
    is_owner = project.get("owner_id") == acting_user_id
    is_admin = acting_user.get("role") == "admin"
    if not (is_owner or is_admin):
        return False

    # Ensure the target user exists
    if user_to_update_id not in USERS:
        return False

    members: List[int] = project.get("members", [])

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Update the project data structure
    project["members"] = members
    return True