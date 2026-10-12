from __future__ import annotations

# Example data structures (replace with real data in your application)
PROJECTS = {
    # project_id: {"owner_id": int, "members": set[int]}
}

USERS = {
    # user_id: {"role": str}  # role can be "admin" or "user"
}


def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    req_user_id : int
        The ID of the user performing the action.
    proj_id : int
        The project to modify.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        The user ID to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input parameters
    if mod not in {"add", "remove"}:
        return False

    # Check that the requester exists
    req_user = USERS.get(req_user_id)
    if not req_user:
        return False

    # Check that the target project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Check that the target user exists
    if mod_user_id not in USERS:
        return False

    # Determine if the requester has permission
    is_admin = req_user.get("role") == "admin"
    is_owner = project["owner_id"] == req_user_id

    if not (is_admin or is_owner):
        return False

    members = project.setdefault("members", set())

    if mod == "add":
        # Prevent adding the owner as a member
        if mod_user_id == project["owner_id"]:
            return False
        # Avoid duplicate entries
        if mod_user_id in members:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False
        members.remove(mod_user_id)

    # If we reach here, the operation succeeded
    return True