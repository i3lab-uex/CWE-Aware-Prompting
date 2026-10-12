# update_project_members.py

from typing import Dict, List

# Example data structures (replace with actual data in real usage)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id : {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id : "admin" or "user"
}


def update_project_members(
    acting_user_id: int,
    project_identifier: int,
    modification: str,
    user_to_update_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the modification.
    project_identifier : int
        The ID of the target project.
    modification : str
        Either 'add' or 'remove'.
    user_to_update_id : int
        The ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If an argument is invalid or missing.
    """
    # Basic input validation
    if modification not in {"add", "remove"}:
        raise ValueError("modification must be 'add' or 'remove'")
    if project_identifier not in PROJECTS:
        raise ValueError("Project does not exist")
    if acting_user_id not in USERS:
        raise ValueError("Acting user does not exist")
    if user_to_update_id not in USERS:
        raise ValueError("User to update does not exist")

    project = PROJECTS[project_identifier]
    owner_id: int = project["owner_id"]
    members: List[int] = project["members"]

    # Authorization check
    if acting_user_id != owner_id and USERS[acting_user_id] != "admin":
        # Not the owner nor an admin – deny access
        return False

    if modification == "add":
        # Avoid duplicate entries
        if user_to_update_id in members:
            return False  # Already a member; no change
        members.append(user_to_update_id)
    else:  # modification == "remove"
        if user_to_update_id not in members:
            return False  # User not a member; nothing to remove
        members.remove(user_to_update_id)

    return True


# Example usage (comment out or remove in production)
if __name__ == "__main__":
    # Populate example data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({100: {"owner_id": 2, "members": [3]}})

    print(update_project_members(1, 100, "add", 2))   # True (admin adding owner)
    print(update_project_members(3, 100, "remove", 2)) # False (not owner/admin)
    print(update_project_members(2, 100, "remove", 3)) # True (owner removing member)