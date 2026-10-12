# ──────────────────────────────────────
#   Project Participant Management
# ──────────────────────────────────────

from typing import Dict, Set

# Example data structures (replace with real ones in production)
PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    # project_id: { 'owner_id': int, 'members': set of user_ids }
}
USERS: Dict[int, str] = {
    # user_id: 'admin' or 'user'
}

def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the operation.
    prj_id : int
        The project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The user ID to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        return False

    # Validate project existence
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Check acting user role
    acting_role = USERS.get(acting_user_id)
    if not acting_role:
        return False

    is_owner = project.get("owner_id") == acting_user_id
    is_admin = acting_role.lower() == "admin"

    if not (is_owner or is_admin):
        return False

    members = project.get("members")
    if members is None:
        # Initialize the set if missing
        project["members"] = members = set()

    try:
        if action_type == "add":
            members.add(target_id)
        else:  # remove
            members.discard(target_id)  # discard does nothing if target not present
        return True
    except Exception:
        # Any unexpected error results in a failure
        return False

# ──────────────────────────────────────