# -*- coding: utf-8 -*-
"""
Project membership management module.

The `handle_project_membership` function allows a user to add or remove
team members from a project.  Only the project owner or an administrator
may perform this action.

Author: ChatGPT
"""

from typing import Dict, List

# Example data structures (replace with real persistence in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id : "user" or "admin"
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
        ID of the user performing the action.
    proj_id : int
        ID of the project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic input validation
    if operation not in {"add", "remove"}:
        return False

    # Retrieve user role; treat unknown users as normal users
    user_role = USERS.get(active_user_id, "user")

    # Retrieve project; if not found, cannot modify
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Authorization: only owner or admin may modify
    if user_role != "admin" and project.get("owner_id") != active_user_id:
        return False

    members = project.setdefault("members", [])

    if operation == "add":
        # Avoid duplicates
        if target_member_id not in members:
            members.append(target_member_id)
            return True
        else:
            # Member already present; consider as success
            return True

    if operation == "remove":
        # Remove only if present
        try:
            members.remove(target_member_id)
            return True
        except ValueError:
            # Member not found; treat as failure to modify
            return False

    # Should never reach here
    return False


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Setup sample data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({101: {"owner_id": 2, "members": [3]}})

    # Admin adds a member
    print(handle_project_membership(1, 101, "add", 4))   # True
    # Owner removes a member
    print(handle_project_membership(2, 101, "remove", 3))  # True
    # Unauthorized user attempts action
    print(handle_project_membership(3, 101, "add", 5))   # False