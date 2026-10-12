import threading

# Global data structures (example)
PROJECTS = {
    # project_id: {"owner_id": int, "members": set(int)}
}
USERS = {
    # user_id: "admin" or "user"
}

# A lock to protect concurrent modifications of PROJECTS
_project_lock = threading.RLock()


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Allows an active user to add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project identifier to be updated.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID of the member to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action_type early
    if action_type not in {"add", "remove"}:
        return False

    # Quick existence checks
    with _project_lock:
        project = PROJECTS.get(prj_id)
        if not project:
            return False

        # Check that the target member exists in USERS
        if member_user_id not in USERS:
            return False

        # Permission check: admin or project owner
        if USERS.get(active_user_id) != "admin":
            if active_user_id != project["owner_id"]:
                return False

        members = project.setdefault("members", set())

        if action_type == "add":
            # Avoid adding duplicates
            if member_user_id in members:
                return False
            members.add(member_user_id)
        else:  # action_type == "remove"
            if member_user_id not in members:
                return False
            members.remove(member_user_id)

    return True