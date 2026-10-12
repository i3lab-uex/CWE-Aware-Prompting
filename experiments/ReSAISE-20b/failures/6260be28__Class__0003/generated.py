#!/usr/bin/env python3
"""
Project management helper for modifying project settings.

This module contains a single public function:
    modify_project_settings(user_id, user_role, project_id, new_settings)

The function performs proper authorization checks and updates the in-memory
PROJECTS_DB dictionary.  It follows best practices to avoid common
authorization pitfalls such as CWE‑863.
"""

from __future__ import annotations

import copy
from typing import Dict, Any


# In‑memory database of projects.  Each project contains:
#   - project_id: str
#   - creator_id: str
#   - members: list[str]
#   - settings: dict
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def _is_authorized(user_id: str, user_role: str, project: Dict[str, Any]) -> bool:
    """
    Determine if a user is authorized to modify project settings.

    Authorization policy:
        * Project managers (user_role == 'project_manager') are allowed.
        * The creator of the project is implicitly a manager.
        * No other roles are permitted.

    Args:
        user_id: The ID of the user.
        user_role: The role of the user in the system.
        project: The project dictionary.

    Returns:
        True if authorized, False otherwise.
    """
    # Explicit role check first
    if user_role == "project_manager":
        return True

    # Implicitly allow the creator of the project
    if user_id == project.get("creator_id"):
        return True

    # All other cases are not authorized
    return False


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Args:
        user_id: ID of the user attempting the change.
        user_role: Role of the user ('project_manager', 'team_member', or 'viewer').
        project_id: ID of the target project.
        new_settings: Dictionary containing new settings to apply.

    Returns:
        A confirmation string if the update succeeds.

    Raises:
        ValueError: If the project does not exist or new_settings is not a dict.
    """
    # Validate input types
    if not isinstance(new_settings, dict):
        raise ValueError("new_settings must be a dictionary")

    # Retrieve the project from the in-memory database
    project = PROJECTS_DB.get(project_id)
    if project is None:
        raise ValueError(f"Project '{project_id}' does not exist")

    # Authorization check
    if not _is_authorized(user_id, user_role, project):
        return "Authorization error: insufficient permissions to modify settings."

    # Make a defensive copy of the existing settings and merge
    updated_settings = copy.deepcopy(project.get("settings", {}))
    updated_settings.update(new_settings)

    # Persist the changes back to the in-memory database
    project["settings"] = updated_settings

    return (
        f"Project '{project_id}' settings successfully updated by user "
        f"'{user_id}'. New settings: {updated_settings}"
    )


# Example usage (commented out to avoid execution on import)
if __name__ == "__main__":
    try:
        result = modify_project_settings(
            user_id="user_a",
            user_role="project_manager",
            project_id="proj_001",
            new_settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(result)
    except ValueError as exc:
        print(f"Error: {exc}")