#!/usr/bin/env python3
"""
Project preference updater for a shared project management platform.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# Simulated in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"theme": "light", "notifications": True},
    },
    # Additional projects can be added here.
}


def _has_write_permission(member_id: str, member_role: str, project: Dict[str, Any]) -> bool:
    """
    Determine if the member has permission to modify project settings.

    Args:
        member_id: The ID of the user attempting the change.
        member_role: The role of that user (e.g., 'project_manager', 'team_member', 'viewer').
        project: The project record from the database.

    Returns:
        True if the member is allowed to modify settings, False otherwise.
    """
    # Only project managers or the creator are granted write access.
    if member_role != "project_manager":
        return False

    # The creator is implicitly a project manager.
    if member_id == project["creator_id"]:
        return True

    # The user must be listed as a member of the project.
    return member_id in project["members"]


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project after performing proper access control checks.

    Args:
        member_id: ID of the user attempting to modify settings.
        member_role: Role of that user in the system.
        proj_id: ID of the project to be updated.
        fresh_settings: Dictionary containing settings that should replace or augment existing ones.

    Returns:
        A success message string upon successful update.

    Raises:
        PermissionError: If the user does not have permission to modify the project.
        KeyError: If the specified project ID does not exist in the database.
    """
    # Retrieve the target project; KeyError will propagate if missing.
    project = PROJECTS_DB[proj_id]

    # Enforce access control
    if not _has_write_permission(member_id, member_role, project):
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized "
            f"to modify settings for project '{proj_id}'."
        )

    # Perform a deep copy to avoid mutating the input dictionary.
    new_settings = copy.deepcopy(fresh_settings)

    # Merge settings: existing keys are overwritten, new keys added.
    project["settings"].update(new_settings)

    return f"Project '{proj_id}' settings successfully updated."


# Example usage (commented out for production use)
if __name__ == "__main__":
    try:
        msg = alter_project_preferences(
            member_id="user-123",
            member_role="project_manager",
            proj_id="proj-001",
            fresh_settings={"notifications": False, "deadline": "2026-12-31"},
        )
        print(msg)
    except PermissionError as e:
        print(f"Permission error: {e}")
    except KeyError as e:
        print(f"Project not found: {e}")