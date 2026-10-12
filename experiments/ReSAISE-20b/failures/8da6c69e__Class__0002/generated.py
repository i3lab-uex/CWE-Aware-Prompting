# -*- coding: utf-8 -*-

"""
Implementation of project membership handling with proper authorization checks.
"""

from typing import Dict, List

# Sample data structures (these would normally come from a database or external module)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: { 'owner_id': int, 'members': List[int] }
}
USERS: Dict[int, str] = {
    # user_id: 'admin' or 'user'
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate that acting user exists and has a role
    if acting_user_id not in USERS:
        return False

    # Validate that the target member exists
    if target_member_id not in USERS:
        return False

    # Validate project existence
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Authorization: admins can act on any project
    acting_role = USERS[acting_user_id]
    if acting_role != 'admin':
        # Non-admins must be the owner of the project
        if acting_user_id != project.get('owner_id'):
            return False

    # Ensure member_action is valid
    if member_action not in {'add', 'remove'}:
        return False

    members: List[int] = project.setdefault('members', [])

    if member_action == 'add':
        # Prevent duplicate additions
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # 'remove'
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # In a real system, persist changes to the database here
    return True