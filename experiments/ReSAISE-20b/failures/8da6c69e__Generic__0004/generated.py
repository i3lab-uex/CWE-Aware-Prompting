from typing import Dict, List

# Example global data structures (should be provided elsewhere in the application)
PROJECTS: Dict[int, Dict[str, any]] = {
    # project_id: {'owner_id': int, 'members': List[int]}
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
        The ID of the user performing the action.
    prjt_id : int
        The ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Validate acting user role
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Determine permission
    is_owner = project.get('owner_id') == acting_user_id
    has_permission = (acting_role == 'admin') or is_owner

    if not has_permission:
        return False

    # Validate action type
    if member_action not in ('add', 'remove'):
        raise ValueError(f"Invalid member_action: {member_action!r}")

    members = project.setdefault('members', [])

    if member_action == 'add':
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # remove
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    return True