# handle_project_membership.py

from typing import Dict, List


# Example data structures; in a real application these would be persisted
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the operation.
    prjt_id : int
        The project whose membership is being modified.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user ID of the member to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input arguments
    if member_action not in {"add", "remove"}:
        return False

    # Check that both users exist
    if acting_user_id not in USERS or target_member_id not in USERS:
        return False

    # Check that the project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Authorization: admins can do anything
    acting_role = USERS.get(acting_user_id)
    if acting_role == "admin":
        authorized = True
    else:
        # Non-admins must be the project owner
        authorized = acting_user_id == project.get("owner_id")

    if not authorized:
        return False

    # Perform the action
    members: List[int] = project.get("members", [])

    if member_action == "add":
        if target_member_id not in members:
            members.append(target_member_id)
            project["members"] = members
        # If already a member, consider it successful
    else:  # remove
        if target_member_id in members:
            members.remove(target_member_id)
            project["members"] = members
        # If not a member, consider it successful

    return True


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    # Setup sample data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({101: {"owner_id": 2, "members": [3]}})

    # Admin adds a member
    print(handle_project_membership(1, 101, "add", 3))  # True

    # Owner removes a member
    print(handle_project_membership(2, 101, "remove", 3))  # True

    # Unauthorized user attempts to add
    print(handle_project_membership(3, 101, "add", 2))  # False