# -*- coding: utf-8 -*-
"""
Module providing project membership management.

This implementation protects against improper access control (CWE‑284)
by ensuring that only project owners or users with the 'admin' role
can modify membership lists. It also performs basic validation of
input parameters and guards against common pitfalls such as
adding a user that is already a member or removing one that does not exist.
"""

from typing import Dict, List

# Example in‑memory data stores (replace with real persistence in production)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {'owner_id': int, 'members': [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id : 'admin' | 'user'
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
        ID of the user performing the operation.
    project_identifier : int
        ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        ID of the member to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate modification type early
    if modification not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Retrieve acting user's role; default to 'user' if unknown
    role = USERS.get(acting_user_id, "user")

    # Permission check: only owner or admin can modify
    if role != "admin" and acting_user_id != project["owner_id"]:
        return False

    members = project.get("members", [])

    # Ensure the target user exists in USERS to avoid dangling references
    if user_to_update_id not in USERS:
        return False

    # Perform the requested modification
    if modification == "add":
        if user_to_update_id in members:
            # Already a member; nothing to do but still considered success
            return True
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            # Not a member; cannot remove
            return False
        members.remove(user_to_update_id)

    # Persist the updated list back to the project dictionary
    project["members"] = members

    return True


# --- Example usage (for testing purposes) ---
if __name__ == "__main__":
    # Setup dummy data
    USERS.update({
        1: "admin",
        2: "user",
        3: "user",
    })
    PROJECTS.update({
        101: {"owner_id": 2, "members": [3]},
    })

    # Admin adding a user
    assert update_project_members(1, 101, "add", 4) is False  # user 4 doesn't exist

    USERS[4] = "user"
    assert update_project_members(1, 101, "add", 4) is True
    assert 4 in PROJECTS[101]["members"]

    # Owner removing a user
    assert update_project_members(2, 101, "remove", 3) is True
    assert 3 not in PROJECTS[101]["members"]

    # Unauthorized user attempting to modify
    assert update_project_members(3, 101, "add", 2) is False

    print("All tests passed.")