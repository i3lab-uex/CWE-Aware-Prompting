from typing import Dict, Set

# Sample data structures. In a real system these would be populated from a database.
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: {"owner_id": int, "members": set of user_ids}
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 15, "members": {25}},
}

USERS: Dict[int, str] = {
    # user_id: role ("admin" or "user")
    10: "admin",
    15: "user",
    20: "user",
    25: "admin",
    30: "user",
}


def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the operation.
    proj_id : int
        ID of the project to modify.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic input validation
    if mod not in {"add", "remove"}:
        return False

    # Ensure the target project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Authorization check: admin or owner
    req_user_role = USERS.get(req_user_id)
    if req_user_role != "admin" and req_user_id != project["owner_id"]:
        return False

    # Ensure the user to modify exists
    if mod_user_id not in USERS:
        return False

    members = project["members"]

    if mod == "add":
        # Adding an existing member is a no-op but considered successful
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False
        members.remove(mod_user_id)

    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    print(handle_project_membership(10, 1, "add", 25))   # True (admin adding)
    print(handle_project_membership(15, 1, "remove", 20)) # False (not owner or admin)
    print(handle_project_membership(10, 1, "remove", 20)) # True (admin removing)