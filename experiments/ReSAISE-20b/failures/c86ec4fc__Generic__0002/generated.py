from __future__ import annotations

from typing import Dict, List, Set


# Example data structures – in a real system these would be loaded from a database
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "user",
}

PROJECTS: Dict[int, Dict[str, object]] = {
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Allow a project owner or an administrator to add or remove members from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        ID of the project being modified.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If any argument is invalid (unknown user, project or action type).
    """
    # Validate existence of acting user
    if acting_user_id not in USERS:
        raise ValueError(f"Acting user {acting_user_id} does not exist")

    # Validate existence of target user
    if target_id not in USERS:
        raise ValueError(f"Target user {target_id} does not exist")

    # Validate project
    if prj_id not in PROJECTS:
        raise ValueError(f"Project {prj_id} does not exist")

    # Validate action type
    if action_type not in {"add", "remove"}:
        raise ValueError(f"Invalid action type: {action_type}")

    project = PROJECTS[prj_id]
    owner_id: int = project["owner_id"]
    members: Set[int] = project.setdefault("members", set())

    # Permission check
    is_admin = USERS.get(acting_user_id) == "admin"
    is_owner = acting_user_id == owner_id

    if not (is_admin or is_owner):
        # No permission
        return False

    # Perform action
    if action_type == "add":
        members.add(target_id)
        return True

    # action_type == "remove"
    if target_id in members:
        members.remove(target_id)
        return True

    # Nothing to remove
    return False


# Example usage:
if __name__ == "__main__":
    # Admin adding a user to project 101
    print(control_project_participants(1, 101, "add", 4))   # True

    # Owner removing a member
    print(control_project_participants(2, 101, "remove", 3)) # True

    # Unauthorized user attempting to add
    print(control_project_participants(3, 101, "add", 4))   # False