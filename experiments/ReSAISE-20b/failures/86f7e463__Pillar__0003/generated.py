# ────────────────────────────────────────────────────────
#  update_project_members.py
# ────────────────────────────────────────────────────────

from typing import Dict, List

# Sample data structures
PROJECTS: Dict[int, Dict[str, object]] = {
    # project_id: {"owner_id": int, "members": List[int]}
}

USERS: Dict[int, str] = {
    # user_id: "admin" or "user"
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
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic input validation
    if modification not in {"add", "remove"}:
        return False

    # Verify that the acting user exists
    if acting_user_id not in USERS:
        return False

    # Verify that the target project exists
    project = PROJECTS.get(project_identifier)
    if not project:
        return False

    # Verify that the user to be updated exists
    if user_to_update_id not in USERS:
        return False

    # Access control: only project owner or admins can modify
    is_admin = USERS[acting_user_id] == "admin"
    is_owner = project.get("owner_id") == acting_user_id
    if not (is_admin or is_owner):
        return False

    members: List[int] = project.setdefault("members", [])

    if modification == "add":
        # Prevent duplicate addition
        if user_to_update_id in members:
            return False
        members.append(user_to_update_id)
    else:  # modification == "remove"
        # Cannot remove the owner via this function
        if user_to_update_id == project.get("owner_id"):
            return False
        try:
            members.remove(user_to_update_id)
        except ValueError:
            # User was not a member
            return False

    return True