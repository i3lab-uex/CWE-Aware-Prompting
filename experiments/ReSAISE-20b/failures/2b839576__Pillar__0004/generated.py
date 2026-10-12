# project_access_control.py

from typing import Dict, List

# Example data structures (these would normally be populated elsewhere)
PROJECTS: Dict[int, Dict[str, any]] = {
    # project_id : { 'owner_id': int, 'members': List[int] }
}

USERS: Dict[int, str] = {
    # user_id : 'admin' or 'user'
}


def project_access_control(
    active_user_id: int,
    prj_id: int,
    action_type: str,
    member_user_id: int
) -> bool:
    """
    Add or remove a user from a project's member list.

    Parameters
    ----------
    active_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project being updated.
    action_type : str
        Either 'add' or 'remove'.
    member_user_id : int
        The user ID of the target member.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action_type
    if action_type not in {"add", "remove"}:
        raise ValueError("action_type must be 'add' or 'remove'")

    # Verify that the active user exists
    if active_user_id not in USERS:
        return False

    # Verify that the target user exists
    if member_user_id not in USERS:
        return False

    # Verify that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Determine permission
    role = USERS[active_user_id]
    is_owner = project.get("owner_id") == active_user_id
    if role != "admin" and not is_owner:
        # Not an admin and not the owner: deny
        return False

    members: List[int] = project.setdefault("members", [])

    if action_type == "add":
        # Avoid duplicate entries
        if member_user_id in members:
            return False
        members.append(member_user_id)
    else:  # action_type == "remove"
        if member_user_id not in members:
            return False
        members.remove(member_user_id)

    # Operation succeeded
    return True