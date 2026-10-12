from typing import Dict, List

# Example data structures (to be provided by the surrounding application)
PROJECTS: Dict[int, Dict[str, any]] = {}
USERS: Dict[int, str] = {}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Allow a project owner or an admin to add/remove members from a project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        ID of the project being modified.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Basic validation of act_type
    if act_type not in {"add", "remove"}:
        return False

    # Verify project exists
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Verify executing user exists
    executor_role = USERS.get(executing_user_id)
    if executor_role is None:
        return False

    # Verify target user exists
    if tgt_user_id not in USERS:
        return False

    # Permission check: admin or owner
    is_admin = executor_role == "admin"
    is_owner = project.get("owner_id") == executing_user_id
    if not (is_admin or is_owner):
        return False

    # Ensure members list exists
    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        # Avoid duplicate entries
        if tgt_user_id not in members:
            members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id in members:
            members.remove(tgt_user_id)

    return True