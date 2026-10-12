import typing

# Sample data structures (replace with actual data in production)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id : {'owner_id': int, 'members': set[int]}
}

USERS: dict[int, dict[str, typing.Any]] = {
    # user_id : {'role': 'admin' | 'user'}
}


def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Modify project membership.

    Args:
        req_user_id: ID of the user performing the action.
        proj_id: Project to modify.
        mod: Either 'add' or 'remove'.
        mod_user_id: ID of the user to add/remove.

    Returns:
        True if operation succeeded, False otherwise.
    """
    # Validate action
    if mod not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure target user exists
    if mod_user_id not in USERS:
        return False

    # Authorization: admin or owner
    requester = USERS.get(req_user_id)
    if not requester:
        return False

    is_admin = requester.get("role") == "admin"
    is_owner = project["owner_id"] == req_user_id

    if not (is_admin or is_owner):
        return False

    members: set[int] = project.setdefault("members", set())

    if mod == "add":
        # Prevent adding duplicate or owner as member
        if mod_user_id in members or mod_user_id == project["owner_id"]:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False
        members.remove(mod_user_id)

    # Operation successful
    return True