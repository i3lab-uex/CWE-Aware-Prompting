from typing import Dict, List

# Sample data structures (these would normally be populated elsewhere in the application)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # Example:
    # 1: {"owner_id": 101, "members": [102, 103]},
}
USERS: Dict[int, str] = {
    # Example:
    # 101: "admin",
    # 102: "user",
    # 103: "user",
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
        ID of the user performing the operation.
    proj_id : int
        ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation of input types and values
    if not isinstance(active_user_id, int) or not isinstance(proj_id, int) \
       or not isinstance(target_member_id, int):
        return False

    if operation not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Verify that the active user exists and determine their role
    role = USERS.get(active_user_id)
    if not role:
        return False

    # Only admins or the project owner may modify membership
    if role != "admin" and active_user_id != project.get("owner_id"):
        return False

    members: List[int] = project.setdefault("members", [])

    if operation == "add":
        # Avoid duplicate members
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Optional: persist changes if using a database or external storage
    return True