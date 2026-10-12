# adjust_team_membership.py

from typing import Dict, List

# Example data structures (these would normally be loaded from a database)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": []},
}
USERS: Dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    30: "user",
}

def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        ID of the target project.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Validate operation type
    if operation_type not in {"add", "remove"}:
        return False

    # Validate operator role
    operator_role = USERS.get(operator_id)
    if operator_role is None:
        return False

    # Only project owner or admin can modify membership
    if operator_role != "admin" and operator_id != project["owner_id"]:
        return False

    # Ensure member exists
    if member_id not in USERS:
        return False

    members = project["members"]

    if operation_type == "add":
        # Prevent duplicate entries
        if member_id in members:
            return False
        members.append(member_id)
    else:  # operation_type == "remove"
        if member_id not in members:
            return False
        members.remove(member_id)

    # If we reach here, the operation succeeded
    return True

# Example usage (for testing purposes only)
if __name__ == "__main__":
    print(adjust_team_membership(10, 1, "add", 40))   # False (user 40 doesn't exist)
    print(adjust_team_membership(10, 1, "add", 20))   # False (already a member)
    print(adjust_team_membership(10, 1, "remove", 20)) # True