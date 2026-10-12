# project_access_control.py

# Sample data structures for illustration. In a real system these would be
# loaded from persistent storage or an ORM.
PROJECTS = {
    # project_id: { 'owner_id': int, 'members': list[int] }
}

USERS = {
    # user_id: role ('admin' or 'user')
}


def project_access_control(active_user_id: int,
                           prj_id: int,
                           action_type: str,
                           member_user_id: int) -> bool:
    """
    Adds or removes a member from a project, enforcing proper authorization.

    Parameters
    ----------
    active_user_id : int
        The user performing the operation.
    prj_id : int
        The ID of the project to modify.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID of the target member.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Fetch the active user's role
    user_role = USERS.get(active_user_id)
    if not user_role:
        return False

    # Authorization: admin can always act, owner can act on their own project
    if user_role != "admin" and active_user_id != project["owner_id"]:
        return False

    # Validate that the target user exists
    if member_user_id not in USERS:
        return False

    members = project["members"]

    # Perform the action
    if action_type == "add":
        if member_user_id in members:
            # Already a member; consider this a no-op success
            return True
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            # Not a member; consider this a no-op success
            return True
        members.remove(member_user_id)

    # Persist changes (in this simplified example we just modify the dict)
    project["members"] = members
    return True