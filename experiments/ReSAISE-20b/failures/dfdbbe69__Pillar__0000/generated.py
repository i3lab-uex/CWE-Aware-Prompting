from __future__ import annotations

# Sample data structures – in a real system these would be persistent storage.
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
    mod_user_id: int
) -> bool:
    """
    Allows a project owner or an administrator to add or remove members from a project.

    Parameters
    ----------
    req_user_id : int
        The user performing the action.
    proj_id : int
        The project being modified.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate parameters
    if mod not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure the user to modify exists
    if mod_user_id not in USERS:
        return False

    # Determine permission: admin or owner
    req_user = USERS.get(req_user_id)
    if not req_user:
        return False

    is_admin = req_user.get("role") == "admin"
    is_owner = project["owner_id"] == req_user_id

    if not (is_admin or is_owner):
        # Unauthorized attempt
        return False

    members = project.setdefault("members", set())

    if mod == "add":
        # Avoid adding the owner again
        if mod_user_id == project["owner_id"]:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id in members:
            members.remove(mod_user_id)
        else:
            # Trying to remove a non‑member – treat as failure
            return False

    return True