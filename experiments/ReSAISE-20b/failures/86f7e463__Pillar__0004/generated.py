# -*- coding: utf-8 -*-

"""
Project membership management module.
"""

from typing import Dict, List

# Example data structures – in a real system these would be populated elsewhere
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "admin",
}

PROJECTS: Dict[int, Dict[str, List[int]]] = {
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
    Add or remove a user from a project's membership list.

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
        True if the operation succeeded, False otherwise.
    """
    # Validate existence of acting user and target user
    if acting_user_id not in USERS:
        return False  # Acting user does not exist

    if user_to_update_id not in USERS:
        return False  # Target user does not exist

    # Validate project existence
    if project_identifier not in PROJECTS:
        return False  # Project does not exist

    project = PROJECTS[project_identifier]

    # Check access control: admin or owner
    acting_role = USERS.get(acting_user_id)
    if acting_role != "admin" and project["owner_id"] != acting_user_id:
        return False  # Unauthorized

    # Normalize modification string
    mod = modification.strip().lower()
    if mod not in {"add", "remove"}:
        return False  # Invalid modification command

    members = project["members"]

    if mod == "add":
        if user_to_update_id in members:
            return False  # Already a member
        members.append(user_to_update_id)
    else:  # mod == "remove"
        if user_to_update_id not in members:
            return False  # Not a member
        members.remove(user_to_update_id)

    return True