from __future__ import annotations

# Sample data structures; in a real system these would be replaced with database access.
PROJECTS = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {21}},
}

USERS = {
    10: {"role": "admin"},
    11: {"role": "user"},
    20: {"role": "user"},
    21: {"role": "user"},
    30: {"role": "admin"},
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Add or remove a user from a project, respecting ownership and admin privileges.

    Parameters
    ----------
    acting_user_id : int
        ID of the user performing the action.
    prj_id : int
        Project identifier.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        ID of the user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of input types and values
    if not isinstance(acting_user_id, int) or not isinstance(prj_id, int) \
       or not isinstance(action_type, str) or not isinstance(target_id, int):
        return False

    if action_type not in {"add", "remove"}:
        return False

    # Verify that all involved IDs exist
    if acting_user_id not in USERS or target_id not in USERS:
        return False

    project = PROJECTS.get(prj_id)
    if project is None:
        return False

    # Authorization check: acting user must be admin or owner of the project
    acting_role = USERS[acting_user_id].get("role")
    if acting_role != "admin" and acting_user_id != project["owner_id"]:
        return False

    members = project["members"]

    if action_type == "add":
        # Prevent adding duplicate
        members.add(target_id)
    else:  # action_type == "remove"
        if target_id not in members:
            return False
        members.remove(target_id)

    # Update the project entry (in this example the dict is mutable)
    PROJECTS[prj_id]["members"] = members
    return True

# Example usage:
if __name__ == "__main__":
    print(control_project_participants(10, 1, "add", 21))   # True (admin adding)
    print(control_project_participants(20, 1, "remove", 30)) # False (not owner/admin)
    print(control_project_participants(10, 1, "remove", 30)) # True (admin removing)