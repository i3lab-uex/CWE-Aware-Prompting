#!/usr/bin/env python3
"""
Project permission control module.

The core function `control_project_permissions` allows a user to add or
remove members from a project.  Project owners can modify their own projects,
while users with the 'admin' role have unrestricted access to all projects.
"""

from __future__ import annotations

import logging
from typing import Dict, List

# --------------------------------------------------------------------------- #
# Sample data structures (replace with actual persistence in real use)
# --------------------------------------------------------------------------- #

PROJECTS: Dict[int, Dict[str, object]] = {
    # Example:
    # 1: {"owner_id": 101, "members": [101, 102]},
    # 2: {"owner_id": 202, "members": [202, 203]},
}

USERS: Dict[int, str] = {
    # Example:
    # 101: "user",
    # 202: "admin",
}

# --------------------------------------------------------------------------- #
# Logging configuration
# --------------------------------------------------------------------------- #

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# --------------------------------------------------------------------------- #
# Core function
# --------------------------------------------------------------------------- #

def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        Project ID to modify.
    act_type : str
        Either 'add' or 'remove'.
    tgt_user_id : int
        Target user ID to add or remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Notes
    -----
    * Only admins or project owners may modify a project.
    * Adding an already present member or removing a non‑existent member
      results in False (no operation performed).
    * The function performs minimal validation and logs actions for audit.
    """
    # Validate project existence
    project = PROJECTS.get(prjct_id)
    if not project:
        logging.warning(
            "Project %s does not exist (executed by user %s).",
            prjct_id,
            executing_user_id,
        )
        return False

    # Validate action type
    if act_type not in {"add", "remove"}:
        logging.error(
            "Invalid action type '%s' for project %s by user %s.",
            act_type,
            prjct_id,
            executing_user_id,
        )
        return False

    # Resolve user roles
    executor_role = USERS.get(executing_user_id)
    if executor_role is None:
        logging.warning(
            "Executor user %s not found in USERS.", executing_user_id
        )
        return False

    # Permission check: admin or owner
    is_owner = project.get("owner_id") == executing_user_id
    if executor_role != "admin" and not is_owner:
        logging.warning(
            "User %s (%s) lacks permission to modify project %s.",
            executing_user_id,
            executor_role,
            prjct_id,
        )
        return False

    members: List[int] = project.get("members", [])
    if act_type == "add":
        if tgt_user_id in members:
            logging.info(
                "User %s already a member of project %s.",
                tgt_user_id,
                prjct_id,
            )
            return False
        members.append(tgt_user_id)
        logging.info(
            "User %s added to project %s by user %s.",
            tgt_user_id,
            prjct_id,
            executing_user_id,
        )
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            logging.info(
                "User %s is not a member of project %s; cannot remove.",
                tgt_user_id,
                prjct_id,
            )
            return False
        members.remove(tgt_user_id)
        logging.info(
            "User %s removed from project %s by user %s.",
            tgt_user_id,
            prjct_id,
            executing_user_id,
        )

    # Persist the updated members list
    project["members"] = members
    return True


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Sample data initialization
    PROJECTS[1] = {"owner_id": 101, "members": [101]}
    USERS[101] = "user"
    USERS[202] = "admin"

    # Admin adding a member
    assert control_project_permissions(202, 1, "add", 103) is True

    # Owner removing a member
    assert control_project_permissions(101, 1, "remove", 103) is True

    # Non-owner attempting to modify
    assert control_project_permissions(104, 1, "add", 105) is False

    print("All tests passed.")