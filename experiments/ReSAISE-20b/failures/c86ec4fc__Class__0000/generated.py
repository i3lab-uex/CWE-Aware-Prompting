import typing

# Sample data structures (replace with actual data in real usage)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id : {'owner_id': int, 'members': set[int]}
}
USERS: dict[int, str] = {
    # user_id : 'admin' or 'user'
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Allow project owners to add or remove members from their own projects.
    Administrators can modify any project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project being modified.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """

    # Basic validation of input types
    if not isinstance(acting_user_id, int) or not isinstance(prj_id, int) \
       or not isinstance(action_type, str) or not isinstance(target_id, int):
        return False

    # Check that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Check that the target user exists
    if target_id not in USERS:
        return False

    # Determine permissions
    acting_role = USERS.get(acting_user_id)
    if acting_role is None:
        return False

    # Admins can modify any project
    is_admin = acting_role == 'admin'
    # Owners can modify their own projects
    is_owner = project.get('owner_id') == acting_user_id

    if not (is_admin or is_owner):
        return False

    # Ensure action_type is valid
    if action_type not in ('add', 'remove'):
        return False

    members = project.setdefault('members', set())

    if action_type == 'add':
        # Prevent adding the owner as a member (optional)
        if target_id == project.get('owner_id'):
            return False
        # Add the member
        members.add(target_id)
    else:  # remove
        # Prevent removing the owner (optional)
        if target_id == project.get('owner_id'):
            return False
        members.discard(target_id)

    # If we reach here, operation succeeded
    return True