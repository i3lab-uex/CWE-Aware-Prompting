# -*- coding: utf-8 -*-

"""
Project membership management utilities.
"""

from typing import Dict, List

# Example data structures (these would normally be populated elsewhere in the application)
USERS: Dict[int, str] = {
    # user_id : role
    1: "admin",
    2: "user",
    3: "user",
    4: "user",
}

PROJECTS: Dict[int, Dict] = {
    # project_id : {"owner_id": int, "members": List[int]}
    101: {"owner_id": 2, "members": [3]},
    102: {"owner_id": 4, "members": []},
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types and values
    if not isinstance(acting_user_id, int) or not isinstance(prjt_id, int):
        return False
    if member_action not in {"add", "remove"}:
        return False

    # Ensure the project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Verify the acting user exists
    if acting_user_id not in USERS:
        return False

    # Verify the target member exists
    if target_member_id not in USERS:
        return False

    # Permission check: admin can always modify; owner can modify own project
    acting_role = USERS[acting_user_id]
    if acting_role != "admin" and project["owner_id"] != acting_user_id:
        return False

    members: List[int] = project["members"]

    if member_action == "add":
        # Prevent duplicate addition
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # member_action == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Update the project data structure (in place)
    PROJECTS[prjt_id]["members"] = members
    return True


# Example usage (uncomment to test)
# print(handle_project_membership(1, 101, "add", 4))   # True (admin adding)
# print(handle_project_membership(2, 101, "remove", 3)) # True (owner removing)
# print(handle_project_membership(2, 101, "add", 3))    # False (already a member)