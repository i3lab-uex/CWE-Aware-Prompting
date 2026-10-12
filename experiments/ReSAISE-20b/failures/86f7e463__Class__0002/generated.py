# -*- coding: utf-8 -*-
"""
Module providing project membership management with proper authorization checks.
"""

from typing import Dict, List

# Sample data structures. In a real application these would come from a database.
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "user",
}

PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    100: {"owner_id": 2, "members": [3]},
    101: {"owner_id": 4, "members": []},
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
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
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if modification not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Verify that the acting user exists
    actor_role = USERS.get(acting_user_id)
    if actor_role is None:
        return False

    # Authorization: only admins or the project owner can modify members
    if actor_role != "admin" and acting_user_id != project["owner_id"]:
        return False

    # Verify that the user to update exists
    if user_to_update_id not in USERS:
        return False

    members: List[int] = project["members"]

    if modification == "add":
        # Avoid duplicate additions
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Update the project data structure
    PROJECTS[project_identifier]["members"] = members
    return True