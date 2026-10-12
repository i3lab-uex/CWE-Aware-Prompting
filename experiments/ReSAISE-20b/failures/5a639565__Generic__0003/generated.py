#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Team access management for projects.

The module defines a single public function `manage_team_access` that
allows project owners to add or remove members from their projects,
while administrators can modify any project.  The data is stored in
in‑memory dictionaries `PROJECTS` and `USERS`.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

from typing import Dict, List, Literal, Set

# --------------------------------------------------------------------------- #
# Sample data structures (replace with real persistence in production)
# --------------------------------------------------------------------------- #

# USERS maps user_id -> set of roles ('admin', 'user')
USERS: Dict[int, Set[str]] = {
    1: {"admin"},
    2: {"user"},
    3: {"user"},
    4: {"user"},
}

# PROJECTS maps project_id -> dict with 'owner_id' and list of member_ids
PROJECTS: Dict[int, Dict[str, object]] = {
    101: {"owner_id": 2, "members": [3]},
    102: {"owner_id": 4, "members": []},
}


# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: Literal["add", "remove"],
    target_member_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executor_user_id : int
        ID of the user performing the operation.
    proj_id : int
        The project whose membership is to be changed.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Notes
    -----
    * The executor must be either the project owner or an administrator.
      Non‑admin users cannot modify projects they do not own.
    * Adding a user who is already a member has no effect but still
      returns True.
    * Removing a user who is not a member also has no effect but still
      returns True.
    * The function performs minimal validation and does not raise
      exceptions on failure; it simply returns False.
    """

    # Quick validation of input types and values
    if not isinstance(operation, str) or operation not in {"add", "remove"}:
        return False

    # Ensure the executor exists
    if executor_user_id not in USERS:
        return False

    # Retrieve project data; fail if missing
    proj = PROJECTS.get(proj_id)
    if not proj:
        return False

    # Permission check: admin or project owner
    executor_roles = USERS.get(executor_user_id, set())
    if "admin" not in executor_roles and executor_user_id != proj["owner_id"]:
        return False

    # Ensure the target member exists
    if target_member_id not in USERS:
        return False

    members: List[int] = proj.get("members", [])

    if operation == "add":
        # Add only if not already present
        if target_member_id not in members:
            members.append(target_member_id)
    else:  # operation == "remove"
        if target_member_id in members:
            members.remove(target_member_id)

    # Update the project dictionary
    proj["members"] = members
    return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Admin adding a member
    print(manage_team_access(1, 101, "add", 4))   # True
    print(PROJECTS[101]["members"])

    # Owner removing a member
    print(manage_team_access(2, 101, "remove", 3))  # True
    print(PROJECTS[101]["members"])

    # Unauthorized attempt
    print(manage_team_access(3, 102, "add", 2))   # False