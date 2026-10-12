#!/usr/bin/env python3
"""
Utility to manage project membership with role‑based access control.

The module expects two global dictionaries:

* `PROJECTS`: Mapping of project_id → dict containing
  - 'owner_id': int
  - 'members': set[int]
* `USERS`: Mapping of user_id → dict containing
  - 'role': str   # e.g. "admin" or "user"

The function `manage_project_access` enforces that only the project owner
or an admin may add or remove members.
"""

from __future__ import annotations

from typing import Dict, Set

# Example global data structures (replace with real data in production)
PROJECTS: Dict[int, Dict[str, Set[int] | int]] = {}
USERS: Dict[int, Dict[str, str]] = {}


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int,
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    current_user_id : int
        ID of the user performing the action.
    project_id : int
        ID of the target project.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    KeyError
        If any of the supplied IDs are not present in the corresponding
        dictionaries.
    ValueError
        If `action` is neither 'add' nor 'remove'.
    """
    # Validate existence of involved entities
    if project_id not in PROJECTS:
        raise KeyError(f"Project {project_id} does not exist.")
    if current_user_id not in USERS:
        raise KeyError(f"User {current_user_id} does not exist.")
    if target_user_id not in USERS:
        raise KeyError(f"Target user {target_user_id} does not exist.")

    project = PROJECTS[project_id]
    owner_id: int = project["owner_id"]
    members: Set[int] = project.setdefault("members", set())

    # Permission check
    current_role = USERS[current_user_id]["role"]
    if not (current_user_id == owner_id or current_role.lower() == "admin"):
        return False

    # Normalize action
    action_lower = action.strip().lower()
    if action_lower not in {"add", "remove"}:
        raise ValueError(f"Invalid action '{action}'. Must be 'add' or 'remove'.")

    # Perform the requested operation
    if action_lower == "add":
        if target_user_id in members:
            return False  # already a member
        members.add(target_user_id)
    else:  # action_lower == "remove"
        if target_user_id not in members:
            return False  # cannot remove non‑member
        members.remove(target_user_id)

    return True


# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Setup demo data
    USERS.update(
        {
            1: {"role": "admin"},
            2: {"role": "user"},
            3: {"role": "user"},
        }
    )
    PROJECTS.update(
        {
            101: {"owner_id": 2, "members": {3}},
        }
    )

    # Admin adds user 1 to project 101
    print(manage_project_access(1, 101, "add", 1))  # True
    # Owner removes user 3 from project 101
    print(manage_project_access(2, 101, "remove", 3))  # True
    # Regular user tries to add another member (should fail)
    print(manage_project_access(3, 101, "add", 2))  # False