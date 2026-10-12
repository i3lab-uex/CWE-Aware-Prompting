from typing import Dict, List

# Example data structures (replace with actual application data)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [user_ids]}
}
USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the operation.
    project_identifier : int
        The ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        The ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if modification not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Ensure acting user exists and has a role
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Permission check: admins can modify any project
    if acting_role != "admin":
        # Non-admins must be the owner of the project
        if acting_user_id != project.get("owner_id"):
            return False

    # Retrieve current members list
    members = project.setdefault("members", [])

    if modification == "add":
        # Avoid adding duplicates
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Persist changes (in this in-memory example, nothing more to do)
    return True