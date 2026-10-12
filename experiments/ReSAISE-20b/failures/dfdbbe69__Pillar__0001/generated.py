# -*- coding: utf-8 -*-
"""
Project membership management module.

The main function `handle_project_membership` enforces proper access control:
- Project owners may add or remove members from their own projects.
- Administrators (role == 'admin') can modify any project.

The function returns `True` on success, otherwise `False`.
"""

from __future__ import annotations

# Example data structures. In a real application these would be loaded from a database.
USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
    4: {"role": "user"},
}

PROJECTS = {
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int,
) -> bool:
    """
    Modify project membership.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the action.
    proj_id : int
        Target project ID.
    mod : str
        Action to perform: 'add' or 'remove'.
    mod_user_id : int
        User ID to be added or removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate input types early to avoid accidental misuse
    if not isinstance(req_user_id, int) or not isinstance(proj_id, int):
        return False
    if mod not in {"add", "remove"}:
        return False

    # Fetch requestor and project data
    req_user = USERS.get(req_user_id)
    if req_user is None:
        # Unknown requestor
        return False

    project = PROJECTS.get(proj_id)
    if project is None:
        # Unknown project
        return False

    # Access control: admin or owner
    is_admin = req_user.get("role") == "admin"
    is_owner = project["owner_id"] == req_user_id
    if not (is_admin or is_owner):
        return False

    # Validate target user existence
    if mod_user_id not in USERS:
        return False

    members = project["members"]
    if mod == "add":
        # Avoid adding duplicate
        if mod_user_id in members:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False
        members.remove(mod_user_id)

    # Operation successful
    return True

# Example usage (for demonstration; remove or comment out in production)
if __name__ == "__main__":
    assert handle_project_membership(1, 101, "add", 4) is True   # admin adding
    assert handle_project_membership(2, 101, "remove", 3) is True  # owner removing
    assert handle_project_membership(2, 102, "add", 3) is False   # not owner or admin
    print("All tests passed.")