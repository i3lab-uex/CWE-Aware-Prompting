import typing

# Example data structures; replace with actual data in your application.
PROJECTS: dict[int, dict[str, typing.Any]] = {
    1: {"owner_id": 101, "members": [102, 103]},
    2: {"owner_id": 104, "members": [105]},
}
USERS: dict[int, str] = {
    101: "user",
    102: "user",
    103: "admin",
    104: "user",
    105: "user",
}


def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Args:
        active_user_id (int): ID of the user performing the operation.
        proj_id (int): ID of the project to modify.
        operation (str): Either 'add' or 'remove'.
        target_member_id (int): ID of the user to add/remove.

    Returns:
        bool: True if the operation succeeded, False otherwise.

    Raises:
        ValueError: If an invalid operation is supplied.
    """
    # Validate operation
    if operation not in {"add", "remove"}:
        raise ValueError("operation must be 'add' or 'remove'")

    # Ensure project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Ensure target user exists
    if target_member_id not in USERS:
        return False

    # Determine permission: owner or admin
    is_owner = project["owner_id"] == active_user_id
    is_admin = USERS.get(active_user_id) == "admin"
    if not (is_owner or is_admin):
        return False

    members = project["members"]

    if operation == "add":
        # Avoid duplicate entries
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        # Prevent removing the owner from their own project
        if target_member_id == project["owner_id"]:
            return False
        members.remove(target_member_id)

    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    print(handle_project_membership(101, 1, "add", 105))   # True
    print(handle_project_membership(102, 1, "remove", 103)) # False (not owner/admin)
    print(handle_project_membership(103, 1, "remove", 102)) # True (admin)