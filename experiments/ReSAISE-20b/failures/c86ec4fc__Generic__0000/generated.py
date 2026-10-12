from __future__ import annotations

# Sample data structures (to be replaced with actual database or in‑memory store)
PROJECTS: dict[int, dict[str, set | int]] = {
    # project_id: {"owner_id": int, "members": set[int]}
}

USERS: dict[int, str] = {
    # user_id: "admin" or "user"
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a participant from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types and values
    if action_type not in {"add", "remove"}:
        return False

    project = PROJECTS.get(prj_id)
    if not project:
        # Project does not exist
        return False

    owner_id = project.get("owner_id")
    if owner_id is None:
        return False

    # Check permissions: admin or project owner
    acting_role = USERS.get(acting_user_id)
    if acting_role != "admin" and acting_user_id != owner_id:
        return False

    members: set[int] = project.get("members", set())

    if action_type == "add":
        # Prevent duplicate entries
        if target_id in members:
            return False
        members.add(target_id)
    else:  # action_type == "remove"
        if target_id not in members:
            return False
        members.remove(target_id)

    # Update the project record
    project["members"] = members
    return True