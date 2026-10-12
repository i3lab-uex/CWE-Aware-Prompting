from __future__ import annotations

import threading
from typing import Dict, List, Set

# Example data structures; in real usage these would be populated elsewhere
USERS: Dict[int, Set[str]] = {}  # e.g., {1: {"admin"}, 2: {"user"}}
PROJECTS: Dict[int, Dict[str, object]] = {}  # e.g., {101: {"owner_id": 1, "members": [2, 3]}}

# Thread‑safe lock for modifying shared data
_lock = threading.RLock()


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        The user performing the operation.
    prj_id : int
        Identifier of the project to modify.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The user to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Basic validation of input types
    if not isinstance(acting_user_id, int) or not isinstance(prj_id, int) \
            or not isinstance(target_id, int):
        return False

    if action_type not in {"add", "remove"}:
        return False

    with _lock:
        # Ensure the acting user exists
        if acting_user_id not in USERS:
            return False

        # Ensure the target user exists
        if target_id not in USERS:
            return False

        # Ensure the project exists
        proj = PROJECTS.get(prj_id)
        if not isinstance(proj, dict):
            return False

        owner_id = proj.get("owner_id")
        members = proj.get("members")

        if not isinstance(owner_id, int) or not isinstance(members, list):
            return False

        # Authorization check: admin can modify any project; otherwise only owner
        is_admin = "admin" in USERS[acting_user_id]
        if not (is_admin or acting_user_id == owner_id):
            return False

        # Perform the action
        if action_type == "add":
            if target_id not in members:
                members.append(target_id)
        else:  # action_type == "remove"
            if target_id in members:
                members.remove(target_id)

        # Update the project entry (not strictly necessary as list is mutable)
        PROJECTS[prj_id]["members"] = members

    return True