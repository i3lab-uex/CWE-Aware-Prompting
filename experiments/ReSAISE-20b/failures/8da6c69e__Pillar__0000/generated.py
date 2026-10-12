# -*- coding: utf-8 -*-
"""
Module implementing project membership management with proper access control.
"""

from typing import Dict, List

# Example data structures (these would normally be populated elsewhere in the application)
PROJECTS: Dict[int, Dict] = {
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
        Project ID to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate acting user exists
    if acting_user_id not in USERS:
        return False

    # Validate target member exists (must exist for add or remove)
    if target_member_id not in USERS:
        return False

    # Validate project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Access control: only admins or the owner can modify members
    if USERS[acting_user_id] != 'admin' and acting_user_id != project['owner_id']:
        return False

    # Validate action
    if member_action not in ('add', 'remove'):
        return False

    members: List[int] = project.get('members')
    if members is None:
        # Ensure the members list exists
        project['members'] = []
        members = project['members']

    if member_action == 'add':
        # Do not add duplicates
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # member_action == 'remove'
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    return True