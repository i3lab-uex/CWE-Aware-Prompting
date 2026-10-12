from typing import Dict

# Example data structures (replace with actual ones in production)
PROJECTS: Dict[int, Dict] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": []},
}

USERS: Dict[int, str] = {
    10: "user",
    11: "user",
    12: "admin",
    20: "user",
    30: "user",
}


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int,
) -> bool:
    """
    Allow a user to add or remove members from a project.

    Admins can modify any project; regular users may only modify projects they own.
    Returns True if the operation succeeds, False otherwise.
    """
    # Validate action type
    if action_type not in {"add", "remove"}:
        raise ValueError("action_type must be 'add' or 'remove'")

    # Fetch project and check existence
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Fetch active user role
    active_role = USERS.get(active_user_id)
    if not active_role:
        return False

    # Permission check
    if active_role != "admin" and project["owner_id"] != active_user_id:
        return False

    # Perform action
    members = project["members"]

    if action_type == "add":
        if member_user_id in members:
            # Already a member; treat as success
            return True
        members.append(member_user_id)
    else:  # remove
        try:
            members.remove(member_user_id)
        except ValueError:
            # Member not present; treat as success
            return True

    return True