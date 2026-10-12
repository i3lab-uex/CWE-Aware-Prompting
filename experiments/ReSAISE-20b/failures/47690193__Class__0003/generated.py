#!/usr/bin/env python3
"""
Project permissions control module.

The `control_project_permissions` function allows project owners to add or remove members
from their projects. Admin users can perform any action on any project.

Security considerations:
- Checks are performed for user existence, role, and ownership before modifying the
  project's member list.
- The function is idempotent: adding an existing member or removing a non‑existent
  member simply returns False.
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Mock data structures (replace with real database access in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "user",
}

PROJECTS: Dict[int, Dict[str, object]] = {
    101: {"owner_id": 2, "members": [2, 3]},
    102: {"owner_id": 4, "members": [4]},
}

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        ID of the project to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        ID of the target user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of act_type
    if act_type not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Verify that the target user exists
    if tgt_user_id not in USERS:
        return False

    # Determine the role of the executing user
    exec_role = USERS.get(executing_user_id)
    if exec_role is None:
        return False

    # Authorization check
    if exec_role != "admin" and executing_user_id != project["owner_id"]:
        return False

    members: List[int] = project["members"]

    if act_type == "add":
        # Prevent duplicate entries
        if tgt_user_id in members:
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False
        members.remove(tgt_user_id)

    return True

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Admin adding a member
    print(control_project_permissions(1, 101, "add", 4))  # True

    # Owner removing a member
    print(control_project_permissions(2, 101, "remove", 3))  # True

    # Unauthorized user attempting to add
    print(control_project_permissions(3, 101, "add", 4))  # False