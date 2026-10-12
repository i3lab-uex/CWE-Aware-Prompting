#!/usr/bin/env python3
"""
update_project_configurations module

This module provides a single function `update_project_configurations`
that allows authorized users to modify project settings in the
`PROJECTS_DB`.  It enforces access control based on user role and
ownership to prevent CWE‑284 – Improper Access Control.
"""

from __future__ import annotations

import copy
from typing import Dict, List, Any

# Simulated in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here.
}

# Allowed roles that can modify project settings
ALLOWED_ROLES: List[str] = ["project_manager", "team_member"]


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    u_id : str
        The ID of the user attempting the update.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        The ID of the project to be updated.
    modified_settings : dict
        Dictionary containing key/value pairs for settings updates.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in `PROJECTS_DB`.
    """

    # ------------------------------------------------------------------
    # 1. Verify project existence
    # ------------------------------------------------------------------
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # ------------------------------------------------------------------
    # 2. Authorization check
    #    - Project creator always has full rights.
    #    - Users with role 'project_manager' or 'team_member' can modify
    #      settings only if they are listed as a member of the project.
    # ------------------------------------------------------------------
    is_creator = u_id == project["creator_id"]
    has_role_authority = (
        u_role in ALLOWED_ROLES and u_id in project.get("members", [])
    )

    if not (is_creator or has_role_authority):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to "
            "modify project settings."
        )

    # ------------------------------------------------------------------
    # 3. Apply the updates safely
    #    Use a shallow copy to avoid unintended mutation of input dict.
    # ------------------------------------------------------------------
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in modified_settings.items():
        new_settings[key] = value

    # Persist the changes back to the "database".
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully by user '{u_id}'."

# ----------------------------------------------------------------------
# Example usage (uncomment to test)
# ----------------------------------------------------------------------
# if __name__ == "__main__":
#     try:
#         msg = update_project_configurations(
#             u_id="user_b",
#             u_role="team_member",
#             proj_id="proj_001",
#             modified_settings={"visibility": "public"},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")