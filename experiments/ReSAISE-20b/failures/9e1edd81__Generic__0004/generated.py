# -*- coding: utf-8 -*-
"""
Project membership handler.

The module expects two global dictionaries to exist in the importing
namespace:

PROJECTS : dict[int, dict]
    Mapping from project id to a dictionary containing:
        - 'owner_id': int
        - 'members' : list[int]

USERS : dict[int, str]
    Mapping from user id to a role string. The role can be either
    'user' or 'admin'.
"""

from typing import Dict, List

# These will be provided by the caller; here we only declare them
PROJECTS: Dict[int, Dict[str, List[int] | int]] = {}
USERS: Dict[int, str] = {}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the operation.
    proj_id : int
        The ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of arguments
    if operation not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure the target user exists
    if target_member_id not in USERS:
        return False

    # Permission check: admin can always modify, otherwise must be owner
    active_role = USERS.get(active_user_id)
    if active_role != "admin" and project["owner_id"] != active_user_id:
        return False

    members = project.setdefault("members", [])

    if operation == "add":
        # Do not add duplicates
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Prevent removal of the owner from their own project
        if target_member_id == project["owner_id"]:
            return False
        members.remove(target_member_id)

    # Persist changes (in this simple in-memory model the dict is already updated)
    return True