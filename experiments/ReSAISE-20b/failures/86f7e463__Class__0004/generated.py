# -*- coding: utf-8 -*-
"""
Project membership update utility.

This module provides a single function, `update_project_members`, which
allows project owners or administrators to add or remove users from a
project's membership list.

Security considerations:
- The function performs an explicit authorization check: the acting user
  must either be the owner of the project or have a role of 'admin'.
- The function validates that all IDs refer to existing entries in the
  `USERS` and `PROJECTS` dictionaries before performing any modifications.
- It protects against duplicate additions and ensures that a user cannot be
  removed if they are not currently a member.
"""

from typing import Dict, List

# Example data structures (replace with real data sources in production)
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "user",
}

PROJECTS: Dict[int, Dict[str, List[int] | int]] = {
    101: {"owner_id": 2, "members": [3]},
    102: {"owner_id": 4, "members": []},
}

def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate existence of acting user
    if acting_user_id not in USERS:
        return False

    # Validate existence of target user
    if user_to_update_id not in USERS:
        return False

    # Validate project existence
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Authorization check: owner or admin
    if acting_user_id != project["owner_id"] and USERS[acting_user_id] != "admin":
        return False

    # Ensure modification is one of the allowed values
    if modification not in {"add", "remove"}:
        return False

    members: List[int] = project.get("members", [])

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Persist changes (in this simple example, the dictionary is updated in place)
    project["members"] = members
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(update_project_members(1, 101, "add", 4))   # True (admin adding)
    print(update_project_members(2, 101, "add", 4))   # True (owner adding)
    print(update_project_members(3, 101, "remove", 4)) # False (not owner/admin)