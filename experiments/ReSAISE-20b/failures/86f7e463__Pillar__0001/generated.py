# -*- coding: utf-8 -*-

"""
Module providing project membership management with proper access control.
"""

from typing import Dict, List

# Example in-memory data stores
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id : role ('user' or 'admin')
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.

    Notes
    -----
    - Only project owners or users with role 'admin' may modify membership.
    - The function guards against duplicate additions and ensures that a
      removal only occurs if the user is currently a member.
    - Basic validation of input types and values is performed to avoid
      accidental corruption of the data store.
    """
    # Validate modification type
    if modification not in ("add", "remove"):
        return False

    # Retrieve acting user role
    acting_role = USERS.get(acting_user_id)
    if acting_role is None:
        return False

    # Retrieve project data
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Access control: owner or admin
    is_owner = acting_user_id == project.get("owner_id")
    if not (is_owner or acting_role == "admin"):
        return False

    # Ensure target user exists
    if user_to_update_id not in USERS:
        return False

    members: List[int] = project.setdefault("members", [])

    if modification == "add":
        if user_to_update_id in members:
            return False  # already a member
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False  # cannot remove non‑member
        members.remove(user_to_update_id)

    return True