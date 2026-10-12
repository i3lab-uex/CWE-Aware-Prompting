from typing import Dict, Any

# Example data structures – in a real system these would come from a database
PROJECTS: Dict[int, Dict[str, Any]] = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {31}},
}

USERS: Dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    30: "admin",
    31: "user",
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a user from a project.

    Returns True if the operation succeeded, otherwise False.
    """

    # Basic input validation
    if action_type not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Check that the target user exists
    if target_id not in USERS:
        return False

    # Authorization: allow if acting user is admin or the project owner
    role = USERS.get(acting_user_id)
    if role != "admin" and acting_user_id != project["owner_id"]:
        return False

    members = project.setdefault("members", set())

    if action_type == "add":
        # Adding a member who is already in the project has no effect
        members.add(target_id)
    else:  # action_type == "remove"
        if target_id not in members:
            return False
        members.remove(target_id)

    # Operation successful
    return True