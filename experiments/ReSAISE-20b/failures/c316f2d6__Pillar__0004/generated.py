# manage_project_access.py

from typing import Dict, Any


# Sample data structures (replace with real data in production)
PROJECTS: Dict[int, Dict[str, Any]] = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {21}},
}
USERS: Dict[int, str] = {
    10: "owner",
    11: "owner",
    20: "member",
    21: "member",
    30: "member",
    99: "admin",   # Admin user
}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The ID of the user performing the action.
    project_id : int
        The project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user to add/remove.

    Returns
    -------
    bool
        True if the action succeeded, False otherwise.
    """
    # Validate inputs
    if action not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(project_id)
    if not project:
        return False

    # Get role of current user
    current_role = USERS.get(current_user_id)
    if not current_role:
        return False

    # Admins can modify any project
    is_admin = current_role == "admin"

    # Owners can modify their own projects
    is_owner = current_user_id == project["owner_id"]

    if not (is_admin or is_owner):
        # Not authorized
        return False

    # Ensure target user exists
    if target_user_id not in USERS:
        return False

    members = project["members"]

    if action == "add":
        # Adding a member that is already present is harmless
        members.add(target_user_id)
    else:  # action == "remove"
        # Removing a non-member is harmless
        members.discard(target_user_id)

    return True


# Example usage (for testing only)
if __name__ == "__main__":
    assert manage_project_access(10, 1, "add", 40) is True
    assert 40 in PROJECTS[1]["members"]
    assert manage_project_access(20, 1, "remove", 30) is False  # not owner/admin
    assert manage_project_access(99, 2, "remove", 21) is True   # admin
    print("All tests passed.")