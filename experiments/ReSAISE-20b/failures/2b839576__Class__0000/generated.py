import copy

# Sample data structures (replace with real ones in production)
PROJECTS = {
    # project_id: {"owner_id": int, "members": [int]}
}
USERS = {
    # user_id: {"role": "admin" or "user"}
}

def project_access_control(active_user_id: int,
                           prj_id: int,
                           action_type: str,
                           member_user_id: int) -> bool:
    """
    Add or remove a member from a project, respecting ownership and admin privileges.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project ID to modify.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic input validation
    if action_type not in {"add", "remove"}:
        return False

    # Verify active user exists
    active_user = USERS.get(active_user_id)
    if not active_user:
        return False

    # Retrieve project
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Authorization: admin can proceed; otherwise only owner
    if active_user["role"] != "admin" and project.get("owner_id") != active_user_id:
        return False

    # Ensure member user exists
    if member_user_id not in USERS:
        return False

    members = project.setdefault("members", [])

    if action_type == "add":
        # Avoid duplicate entries
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # remove
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    # Update the project (in-place in this example)
    PROJECTS[prj_id]["members"] = members
    return True