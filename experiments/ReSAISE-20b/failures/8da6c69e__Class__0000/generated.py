# handle_project_membership.py

from typing import Dict, List

# Example data structures (would normally come from a database or config)
USERS: Dict[int, str] = {
    1: 'admin',
    2: 'user',
    3: 'user',
    4: 'admin',
}

PROJECTS: Dict[int, Dict] = {
    101: {'owner_id': 2, 'members': [2, 3]},
    102: {'owner_id': 4, 'members': [4]},
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
        The user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user ID of the member to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation of action type
    if member_action not in {'add', 'remove'}:
        return False

    # Check that the project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Retrieve acting user's role; default to 'user' if unknown
    role = USERS.get(acting_user_id, 'user')

    # Authorization check: only admins or the project owner may modify members
    if role != 'admin' and acting_user_id != project['owner_id']:
        return False

    members: List[int] = project.setdefault('members', [])

    if member_action == 'add':
        # Prevent adding duplicate members
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # member_action == 'remove'
        if target_member_id not in members:
            return False
        # Prevent owner from removing themselves unless they are admin
        if target_member_id == project['owner_id'] and role != 'admin':
            return False
        members.remove(target_member_id)

    # If we reach here, the operation succeeded
    return True