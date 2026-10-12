import sys
from typing import Dict, List

# Example data structures (would normally be loaded from a database or config)
PROJECTS: Dict[int, Dict[str, object]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": []},
}

USERS: Dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    30: "user",
    40: "admin",
}

def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

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
        True if operation succeeded, False otherwise.
    """
    # Validate modification type
    if modification not in {"add", "remove"}:
        return False

    # Ensure project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Ensure acting user exists
    if acting_user_id not in USERS or user_to_update_id not in USERS:
        return False

    # Permission check: admin can always modify
    if USERS.get(acting_user_id) != "admin":
        # Non-admins must own the project
        if project.get("owner_id") != acting_user_id:
            return False

    members: List[int] = project.setdefault("members", [])

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False
        members.remove(user_to_update_id)

    # Persist changes (here we just modify the in-memory dict)
    PROJECTS[project_identifier]["members"] = members
    return True

# Example usage:
if __name__ == "__main__":
    print(update_project_members(10, 1, "add", 40))   # True (admin adding)
    print(update_project_members(11, 1, "remove", 20)) # False (not owner or admin)
    print(update_project_members(10, 1, "remove", 20)) # True