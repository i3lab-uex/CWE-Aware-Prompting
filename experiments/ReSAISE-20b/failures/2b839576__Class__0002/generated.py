# -*- coding: utf-8 -*-
"""
Implementation of project access control with proper authorization checks.

The module defines the `project_access_control` function which allows an active user to
add or remove members from a project.  Only the project owner or users with the
`admin` role may perform these operations.

The function validates input, performs necessary authorization checks and updates
the in-memory data structures.  It returns `True` on success, otherwise `False`.

Author: OpenAI ChatGPT
"""

from typing import Dict, List

# Sample data structures (in a real system these would be persisted in a database)
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
    1: {'owner_id': 10, 'members': [20, 30]},
    2: {'owner_id': 11, 'members': [21, 31]},
}

USERS: Dict[int, str] = {
    # user_id : role
    10: 'user',   # owner of project 1
    11: 'user',   # owner of project 2
    99: 'admin',  # admin user
    20: 'user',
    21: 'user',
    30: 'user',
    31: 'user',
}

def project_access_control(active_user_id: int,
                           prj_id: int,
                           action_type: str,
                           member_user_id: int) -> bool:
    """
    Add or remove a member from a project if the active user is authorized.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project ID to modify.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID of the member to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # 1. Validate existence of project
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # 2. Validate existence of member user
    if member_user_id not in USERS:
        return False

    # 3. Validate action type
    if action_type not in {'add', 'remove'}:
        return False

    # 4. Authorization check: admin or project owner
    user_role = USERS.get(active_user_id)
    if user_role != 'admin' and active_user_id != project['owner_id']:
        return False

    members: List[int] = project.setdefault('members', [])

    # 5. Perform the action
    if action_type == 'add':
        if member_user_id in members:
            # Member already present; nothing to do but consider it a success
            return True
        members.append(member_user_id)
    else:  # action_type == 'remove'
        if member_user_id not in members:
            # Member not present; nothing to do but consider it a success
            return True
        members.remove(member_user_id)

    # 6. Update the project record (in this in-memory example it's already updated)
    return True

# Example usage (for testing only; remove or comment out in production):
if __name__ == "__main__":
    print(project_access_control(10, 1, 'add', 40))   # True (owner adding)
    print(project_access_control(99, 1, 'remove', 20)) # True (admin removing)
    print(project_access_control(20, 1, 'add', 50))   # False (not owner or admin)