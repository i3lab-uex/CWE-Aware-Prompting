# -*- coding: utf-8 -*-
"""
Utility module for project membership management.
"""

from typing import Dict, List

# Example data structures (replace with actual storage in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input arguments
    if modification not in {"add", "remove"}:
        return False

    # Fetch the project
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Fetch the role of the acting user
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    # Check permissions: owner or admin
    is_owner = project.get("owner_id") == acting_user_id
    if not (is_owner or acting_role == "admin"):
        return False

    members: List[int] = project.get("members", [])

    if modification == "add":
        # Prevent duplicate addition
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        # Prevent removing the owner
        if user_to_update_id == project.get("owner_id"):
            return False
        try:
            members.remove(user_to_update_id)
        except ValueError:
            # User not in the list
            return False

    # Persist changes (in this simple example we modify the dict directly)
    project["members"] = members
    return True


# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Setup mock data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({100: {"owner_id": 2, "members": [3]}})

    # Admin adds a user
    print(update_project_members(1, 100, "add", 4))  # Expected: True

    # Owner removes a member
    print(update_project_members(2, 100, "remove", 3))  # Expected: True

    # Non-owner non-admin tries to add
    print(update_project_members(3, 100, "add", 5))  # Expected: False