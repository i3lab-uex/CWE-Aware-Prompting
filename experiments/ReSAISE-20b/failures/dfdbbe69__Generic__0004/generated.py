# -*- coding: utf-8 -*-
"""
Project membership management module.

The main entry point is the `handle_project_membership` function which
allows project owners to add or remove members from their own projects,
while administrators can modify any project.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real persistence layer as needed)
# --------------------------------------------------------------------------- #

# USERS maps user_id to a dict containing the user's role.
USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
    4: {"role": "admin"},
}

# PROJECTS maps project_id to a dict containing the owner and members.
PROJECTS = {
    100: {"owner_id": 2, "members": {3}},
    101: {"owner_id": 4, "members": set()},
}

# --------------------------------------------------------------------------- #
# Utility helpers
# --------------------------------------------------------------------------- #

def _is_admin(user_id: int) -> bool:
    """Return True if the user has administrative privileges."""
    return USERS.get(user_id, {}).get("role") == "admin"

def _project_exists(proj_id: int) -> bool:
    """Check if a project exists."""
    return proj_id in PROJECTS

def _user_exists(user_id: int) -> bool:
    """Check if a user exists."""
    return user_id in USERS

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

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
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate input types early to avoid unexpected errors
    if not all(isinstance(v, int) for v in (req_user_id, proj_id, mod_user_id)):
        return False
    if not isinstance(mod, str) or mod.lower() not in {"add", "remove"}:
        return False

    # Basic existence checks
    if not _project_exists(proj_id) or not _user_exists(mod_user_id):
        return False

    project = PROJECTS[proj_id]
    owner_id = project["owner_id"]
    members: set[int] = project["members"]

    # Permission check: admin or owner
    if not (_is_admin(req_user_id) or req_user_id == owner_id):
        return False

    # Perform the requested modification
    mod = mod.lower()
    if mod == "add":
        # Avoid adding the owner as a member
        if mod_user_id == owner_id:
            return False
        # Add only if not already a member
        members.add(mod_user_id)
    else:  # mod == "remove"
        # Removing the owner is not allowed
        if mod_user_id == owner_id:
            return False
        members.discard(mod_user_id)

    # Update the project data (in this in-memory example it's already updated)
    PROJECTS[proj_id]["members"] = members
    return True

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Admin adding a user to project 101
    print(handle_project_membership(1, 101, "add", 2))  # True
    print(PROJECTS[101]["members"])                    # {2}

    # Non-owner non-admin attempting to remove a member
    print(handle_project_membership(3, 100, "remove", 2))  # False

    # Owner removing a member
    print(handle_project_membership(2, 100, "remove", 3))  # True
    print(PROJECTS[100]["members"])                    # set()