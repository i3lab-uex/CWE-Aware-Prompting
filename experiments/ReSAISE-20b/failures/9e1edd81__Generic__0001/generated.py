import typing

# Example data structures (should be replaced with real data in production)
PROJECTS: dict[int, dict[str, typing.Any]] = {}
USERS: dict[int, str] = {}

def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Modify the membership of a project.

    Parameters
    ----------
    active_user_id : int
        ID of the user performing the operation.
    proj_id : int
        Project identifier to modify.
    operation : str
        'add' or 'remove'.
    target_member_id : int
        User ID to add/remove from the project.

    Returns
    -------
    bool
        True if modification succeeded, False otherwise.
    """
    # Validate input types
    if not all(isinstance(x, int) for x in (active_user_id, proj_id, target_member_id)):
        return False
    if operation not in {"add", "remove"}:
        return False

    # Retrieve project and user role
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    user_role = USERS.get(active_user_id, "user")
    is_owner = project.get("owner_id") == active_user_id
    is_admin = user_role.lower() == "admin"

    # Permission check: only owners or admins may modify
    if not (is_owner or is_admin):
        return False

    members = project.setdefault("members", [])

    # Ensure the target exists in USERS
    if target_member_id not in USERS:
        return False

    try:
        if operation == "add":
            # Avoid duplicate entries
            if target_member_id not in members:
                members.append(target_member_id)
        else:  # operation == "remove"
            if target_member_id in members:
                members.remove(target_member_id)
        return True
    except Exception:
        # Catch unexpected errors (e.g., list mutation failures)
        return False