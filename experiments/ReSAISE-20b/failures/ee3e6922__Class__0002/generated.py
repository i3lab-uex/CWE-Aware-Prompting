#!/usr/bin/env python3
"""
Project configuration update module.

This module defines a single public function `change_project_config` which allows
authorized users to modify the settings of an existing project. The function
performs a strict authorization check based on user role and ownership, and
raises `PermissionError` when the caller is not permitted to perform the update.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# --------------------------------------------------------------------------- #
# Mock database: a dictionary keyed by project ID. Each entry contains:
#
#   - 'project_id': str
#   - 'creator_id': str
#   - 'members': list[str]  # user IDs of members
#   - 'settings': dict      # arbitrary project settings
#
# In a real application this would be replaced with persistent storage.
# --------------------------------------------------------------------------- #
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"name": "Alpha", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}


def _is_authorized(uid: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Internal helper to determine if a user is authorized to modify project settings.

    Authorization rules:
        - The creator of the project (creator_id) is always authorized.
        - A user with role 'project_manager' and who is listed in the project's members
          is authorized.
        - No other roles are permitted to modify settings.

    Args:
        uid: The user ID attempting the change.
        role: The user's role string.
        project: The full project dictionary.

    Returns:
        True if the user is authorized, False otherwise.
    """
    # Creator always has full rights
    if uid == project.get("creator_id"):
        return True

    # Project managers must be part of the project
    if role == "project_manager" and uid in project.get("members", []):
        return True

    return False


def change_project_config(uid: str, role: str, proj: str,
                          settings_update: Dict[str, Any]) -> str:
    """
    Update the configuration of a project if the caller is authorized.

    Args:
        uid: Unique identifier of the user attempting the modification.
        role: Role of the user ('project_manager', 'team_member', or 'viewer').
        proj: Identifier of the project whose settings should be changed.
        settings_update: Dictionary containing updated settings.

    Returns:
        A success message indicating the project has been updated.

    Raises:
        KeyError: If the project ID does not exist in PROJECTS_DB.
        PermissionError: If the user is not authorized to modify the project.
    """
    # Retrieve the target project (raises KeyError if missing)
    project = PROJECTS_DB[proj]

    # Authorization check
    if not _is_authorized(uid, role, project):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform a shallow merge of the settings.
    # We copy to avoid accidental mutation of the incoming dict by callers.
    new_settings = copy.deepcopy(project.get("settings", {}))
    for key, value in settings_update.items():
        new_settings[key] = value

    # Update the project entry
    PROJECTS_DB[proj]["settings"] = new_settings

    return f"Project '{proj}' settings updated successfully."


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        print(change_project_config(
            uid="user_b",
            role="project_manager",
            proj="proj_001",
            settings_update={"deadline": "2025-01-15", "budget": 50000}
        ))
    except Exception as e:
        print(f"Error: {e}")