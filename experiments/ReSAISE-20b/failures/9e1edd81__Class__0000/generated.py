# -*- coding: utf-8 -*-

# Sample data structures for demonstration purposes.
# In a real application these would be replaced by database queries.

PROJECTS = {
    # project_id: {"owner_id": int, "members": set(int)}
}

USERS = {
    # user_id: {"role": "admin" | "user"}
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the operation.
    proj_id : int
        The project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user to be added/removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if operation not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Check that the target user exists
    if target_member_id not in USERS:
        return False

    # Authorization: owner or admin can modify
    user_role = USERS.get(active_user_id, {}).get("role")
    if not user_role:
        return False  # unknown active_user_id

    is_owner = (active_user_id == project["owner_id"])
    is_admin = (user_role.lower() == "admin")

    if not (is_owner or is_admin):
        return False  # missing authorization

    members = project.setdefault("members", set())

    if operation == "add":
        # Prevent adding duplicate or self
        if target_member_id in members or target_member_id == active_user_id:
            return False
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    return True