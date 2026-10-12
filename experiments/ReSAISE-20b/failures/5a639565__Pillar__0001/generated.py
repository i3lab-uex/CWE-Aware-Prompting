#!/usr/bin/env python3
"""
Team access management module.

This module provides the `manage_team_access` function that allows a project owner
to add or remove members from their own projects, while administrators have the
privilege to modify any project.  The function performs rigorous access control
checks to mitigate CWE‑284 (Improper Access Control).
"""

from typing import Dict, Set

# --------------------------------------------------------------------------- #
# Sample data structures (replace or extend with real persistence layer)
# --------------------------------------------------------------------------- #

# USERS maps user_id -> set of roles ('admin', 'user')
USERS: Dict[int, Set[str]] = {
    1: {"admin"},
    2: {"user"},
    3: {"user"},
    4: {"user"},
}

# PROJECTS maps project_id -> dict with 'owner_id' and 'members' (set of user_ids)
PROJECTS: Dict[int, Dict[str, Set[int] | int]] = {
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _has_role(user_id: int, role: str) -> bool:
    """Return True if the user has the specified role."""
    return role in USERS.get(user_id, set())

def _is_owner(project: Dict[str, Set[int] | int], user_id: int) -> bool:
    """Return True if the user is the owner of the project."""
    return project.get("owner_id") == user_id

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        The user performing the action.
    proj_id : int
        The project to modify.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic argument validation
    if not isinstance(executor_user_id, int) or not isinstance(proj_id, int):
        return False
    if operation not in {"add", "remove"}:
        return False
    if not isinstance(target_member_id, int):
        return False

    # Ensure executor exists and has a role
    if executor_user_id not in USERS:
        return False

    # Retrieve the project; fail fast if missing
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Access control: allow if executor is admin or owner
    if not (_has_role(executor_user_id, "admin") or _is_owner(project, executor_user_id)):
        return False

    # Ensure target member exists
    if target_member_id not in USERS:
        return False

    members = project.setdefault("members", set())

    if operation == "add":
        # No-op if already a member
        if target_member_id in members:
            return True
        members.add(target_member_id)
    else:  # operation == "remove"
        if target_member_id not in members:
            return True
        members.remove(target_member_id)

    # Optionally persist changes here (e.g., database commit)
    return True

# --------------------------------------------------------------------------- #
# Example usage (for manual testing only; remove or guard with __name__ == "__main__")
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Admin adding a user to project 101
    print(manage_team_access(1, 101, "add", 4))  # Expected: True
    print(PROJECTS[101]["members"])              # Expected: {3, 4}

    # Owner removing a user
    print(manage_team_access(2, 101, "remove", 3))  # Expected: True
    print(PROJECTS[101]["members"])                # Expected: {4}