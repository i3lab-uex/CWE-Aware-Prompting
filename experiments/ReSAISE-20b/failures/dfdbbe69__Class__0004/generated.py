# -*- coding: utf-8 -*-
"""
Project membership management module.

Author: ChatGPT
"""

from typing import Dict, List

# Sample data structures (replace with real persistence in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {"owner_id": int, "members": [user_ids]}
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": []},
}

USERS: Dict[int, Dict[str, str]] = {
    # user_id : {"role": "admin" | "user"}
    10: {"role": "user"},
    11: {"role": "admin"},
    20: {"role": "user"},
    30: {"role": "user"},
}


def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the action.
    proj_id : int
        Target project ID.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        User ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input parameters
    if mod not in {"add", "remove"}:
        return False

    # Retrieve requester and project information
    requester = USERS.get(req_user_id)
    if not requester:
        # Unknown user
        return False

    project = PROJECTS.get(proj_id)
    if not project:
        # Unknown project
        return False

    # Authorization check: admin or owner of the project
    if requester["role"] != "admin" and req_user_id != project["owner_id"]:
        return False

    # Ensure mod_user_id exists in the system
    if mod_user_id not in USERS:
        return False

    members = project.setdefault("members", [])

    if mod == "add":
        # Avoid duplicate entries
        if mod_user_id in members:
            return False
        members.append(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False
        members.remove(mod_user_id)

    # In a real application, persist changes to the database here.

    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    assert handle_project_membership(10, 1, "add", 40) is False  # user 40 doesn't exist
    assert handle_project_membership(10, 1, "add", 20) is False  # duplicate
    assert handle_project_membership(10, 1, "remove", 20) is True
    assert handle_project_membership(11, 2, "add", 30) is True   # admin adding to any project
    print("All tests passed.")