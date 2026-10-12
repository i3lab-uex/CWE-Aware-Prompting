import threading

# Global data structures (for demonstration purposes)
PROJECTS = {
    # project_id: {'owner_id': int, 'members': set[int]}
}
USERS = {
    # user_id: 'admin' or 'user'
}

# Lock to protect concurrent modifications
_projects_lock = threading.RLock()


def project_access_control(active_user_id: int,
                           prj_id: int,
                           action_type: str,
                           member_user_id: int) -> bool:
    """
    Allow project owners to add or remove members from their projects.
    Admins can manage any project without restrictions.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project being updated.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {'add', 'remove'}:
        raise ValueError("action_type must be either 'add' or 'remove'")

    # Validate user existence
    if active_user_id not in USERS:
        return False

    # Retrieve project safely
    with _projects_lock:
        project = PROJECTS.get(prj_id)
        if not project:
            return False

        # Check permissions
        is_admin = USERS.get(active_user_id) == 'admin'
        is_owner = project.get('owner_id') == active_user_id

        if not (is_admin or is_owner):
            return False

        members = project.setdefault('members', set())

        if action_type == 'add':
            # Prevent duplicate
            if member_user_id in members:
                return False
            members.add(member_user_id)
        else:  # remove
            if member_user_id not in members:
                return False
            members.remove(member_user_id)

    return True