import typing

# Sample data structures (replace with actual data in your application)
PROJECTS: dict[int, dict[str, typing.Any]] = {
    # project_id: {"owner_id": int, "members": set[int]}
}
USERS: dict[int, str] = {
    # user_id: role ("admin", "owner", "member", etc.)
}

def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Allows project owners to add or remove members from their project,
    while admins can modify any project.

    Args:
        current_user_id: ID of the user invoking the function.
        project_id: ID of the project being modified.
        action: 'add' or 'remove'.
        target_user_id: ID of the member being added or removed.

    Returns:
        True if the action succeeded, False otherwise.
    """
    # Validate existence of project and users
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Check that the target user exists
    if target_user_id not in USERS:
        return False

    # Determine permission level of current user
    current_role = USERS.get(current_user_id)
    if current_role == "admin":
        allowed = True
    else:
        # Non-admins can only modify their own project if they are the owner
        allowed = current_user_id == project.get("owner_id")

    if not allowed:
        return False

    members = project.setdefault("members", set())

    # Perform action
    if action == "add":
        if target_user_id in members or target_user_id == project.get("owner_id"):
            # Already a member or owner; no change needed
            return False
        members.add(target_user_id)
        return True

    elif action == "remove":
        # Prevent removal of the owner
        if target_user_id == project.get("owner_id"):
            return False
        if target_user_id not in members:
            return False
        members.remove(target_user_id)
        return True

    # Invalid action string
    return False