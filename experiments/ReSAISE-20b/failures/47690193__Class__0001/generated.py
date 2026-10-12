from typing import Dict, List

# Example data structures (replace with actual application data)
USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "user"
}

PROJECTS: Dict[int, Dict] = {
    101: {"owner_id": 2, "members": [3]},
    102: {"owner_id": 4, "members": []}
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        ID of the target project.
    act_type : str
        'add' to add a member, 'remove' to remove a member.
    tgt_user_id : int
        ID of the user being added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of act_type
    if act_type not in {"add", "remove"}:
        return False

    # Verify the project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Verify the target user exists
    if tgt_user_id not in USERS:
        return False

    # Authorization check: admin or project owner
    executing_role = USERS.get(executing_user_id)
    if executing_role != "admin" and executing_user_id != project["owner_id"]:
        return False

    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        # Avoid duplicate entries
        if tgt_user_id in members:
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            return False
        members.remove(tgt_user_id)

    # Operation succeeded
    return True


# Example usage:
if __name__ == "__main__":
    print(control_project_permissions(1, 101, "add", 4))   # True (admin adds)
    print(control_project_permissions(2, 101, "add", 4))   # True (owner adds)
    print(control_project_permissions(3, 101, "add", 4))   # False (not authorized)
    print(control_project_permissions(2, 101, "remove", 3)) # True (owner removes)
    print(control_project_permissions(2, 101, "remove", 5)) # False (user not a member)