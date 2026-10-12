# -*- coding: utf-8 -*-

from typing import Dict, Set

# Example data structures (replace with real data in production)
USERS: Dict[int, str] = {
    # user_id : role ('admin' or 'user')
    1: "admin",
    2: "user",
    3: "user",
    4: "admin",
}

PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id : {"owner_id": int, "members": set of user_ids}
    101: {"owner_id": 2, "members": {2, 3}},
    102: {"owner_id": 4, "members": {4}},
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project to modify.
    action_type : str
        'add' or 'remove'.
    target_id : int
        User ID to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if action_type not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Ensure acting user exists
    acting_role = USERS.get(acting_user_id)
    if acting_role is None:
        return False

    # Ensure target user exists
    if target_id not in USERS:
        return False

    # Permission check: admin or owner
    if acting_role != "admin" and project["owner_id"] != acting_user_id:
        return False

    members: Set[int] = project["members"]

    if action_type == "add":
        # Prevent adding duplicate
        members.add(target_id)
    else:  # remove
        if target_id not in members:
            return False
        # Optional: prevent removing the owner
        if target_id == project["owner_id"]:
            return False
        members.remove(target_id)

    # Update the project's members set
    project["members"] = members
    return True


# Example usage (uncomment to test)
# print(control_project_participants(2, 101, "add", 4))   # True
# print(control_project_participants(3, 101, "remove", 2)) # False (not owner/admin)