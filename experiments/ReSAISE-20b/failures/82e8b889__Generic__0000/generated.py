# ──────────────────────────────────────────────────────────────
# Project membership management module
# ──────────────────────────────────────────────────────────────

from typing import Dict, List

# Example data structures – in real code these would be loaded from a database
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {"owner_id": int, "members": [int, ...]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
}


def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int
) -> bool:
    """
    Add or remove a user from a project's membership list.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        ID of the project whose membership is being modified.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate project existence
    project = PROJECTS.get(team_project_id)
    if not project:
        return False

    # Verify operator's role
    operator_role = USERS.get(operator_id)
    if not operator_role:
        return False

    # Only admins or the project owner may modify membership
    if operator_role != "admin" and operator_id != project["owner_id"]:
        return False

    # Ensure member exists in the system
    if member_id not in USERS:
        return False

    members = project.setdefault("members", [])

    if operation_type == "add":
        # Prevent duplicate entries
        if member_id in members:
            return False
        members.append(member_id)
        return True

    if operation_type == "remove":
        try:
            members.remove(member_id)
            return True
        except ValueError:
            # Member not present
            return False

    # Unsupported operation_type
    return False


# ──────────────────────────────────────────────────────────────
# Example usage (for testing purposes only)
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Setup demo data
    USERS.update({1: "admin", 2: "user", 3: "user"})
    PROJECTS.update({101: {"owner_id": 2, "members": [3]}})

    # Admin adds a member
    print(adjust_team_membership(1, 101, "add", 3))   # True

    # Owner removes a member
    print(adjust_team_membership(2, 101, "remove", 3))  # True

    # Unauthorized user attempts to modify
    print(adjust_team_membership(3, 101, "add", 2))   # False