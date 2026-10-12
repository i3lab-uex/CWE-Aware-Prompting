# SPDX-License-Identifier: MIT
"""
Project membership management module.

This module provides a single function `handle_project_membership` that allows
project owners or administrators to add or remove members from a project.
The function performs strict access control checks to prevent
unauthorized modifications (CWE-284).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real database access in production)
# --------------------------------------------------------------------------- #

# Mapping of project_id -> dict(owner_id: int, members: list[int])
PROJECTS = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 15, "members": [25]},
}

# Mapping of user_id -> role string ('user' or 'admin')
USERS = {
    10: "user",
    15: "admin",
    20: "user",
    25: "user",
    30: "admin",
}

# --------------------------------------------------------------------------- #
# Utility functions
# --------------------------------------------------------------------------- #

def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id) == "admin"


def _is_project_owner(user_id: int, project: dict) -> bool:
    """Return True if the user is the owner of the given project."""
    return project.get("owner_id") == user_id


def _project_exists(proj_id: int) -> bool:
    """Check if a project with the given ID exists."""
    return proj_id in PROJECTS


def _user_exists(user_id: int) -> bool:
    """Check if a user with the given ID exists."""
    return user_id in USERS


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def handle_project_membership(
    active_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
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
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If any of the IDs are invalid, or if operation is not recognized.
    """

    # Validate input types
    if not all(isinstance(x, int) for x in (active_user_id, proj_id, target_member_id)):
        raise ValueError("User IDs and project ID must be integers.")
    if operation not in {"add", "remove"}:
        raise ValueError("Operation must be 'add' or 'remove'.")

    # Ensure project exists
    if not _project_exists(proj_id):
        return False

    # Ensure target user exists
    if not _user_exists(target_member_id):
        return False

    # Access control: only owner or admin can modify
    project = PROJECTS[proj_id]
    if not (_is_admin(active_user_id) or _is_project_owner(active_user_id, project)):
        return False

    members = project["members"]

    if operation == "add":
        # Prevent duplicate membership
        if target_member_id in members:
            return False
        members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return False
        members.remove(target_member_id)

    # Successful modification
    return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     print(handle_project_membership(10, 1, "add", 25))   # True
#     print(handle_project_membership(20, 1, "remove", 30)) # False (not owner/admin)
#     print(PROJECTS[1])