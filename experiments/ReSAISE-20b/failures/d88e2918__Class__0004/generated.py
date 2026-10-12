#!/usr/bin/env python3
"""
edit_project_settings module

Provides a single function `edit_project_settings` that safely updates
project configuration data stored in an in‑memory dictionary.
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# --------------------------------------------------------------------------- #
# In‑memory project database (mocked for this example)
# --------------------------------------------------------------------------- #

PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_a", "user_b"],
        "settings": {"name": "Alpha", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #

class UnauthorizedAccessError(PermissionError):
    """Raised when a user is not authorized to modify project settings."""
    pass

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _is_authorized(member_id: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Determine if the user has permission to edit project settings.

    Only a project manager or the creator of the project may modify settings.
    The user must also be listed as a member of the project.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user.
    role : str
        Role description (e.g., 'project_manager', 'team_member', 'viewer').
    project : dict
        The project data record.

    Returns
    -------
    bool
        True if the user is authorized, False otherwise.
    """
    # Ensure the user is a member of the project
    if member_id not in project.get("members", []):
        return False

    # Only creators or users with the role 'project_manager' can edit
    if member_id == project.get("creator_id"):
        return True

    # Role-based check
    if role.lower() == "project_manager":
        return True

    return False

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update the settings of a project after performing an authorization check.

    Parameters
    ----------
    member_id : str
        Unique identifier of the user attempting the update.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    project_key : str
        Identifier of the target project.
    updated_configuration : dict
        Dictionary containing the new settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    UnauthorizedAccessError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project key does not exist in `PROJECTS_DB`.
    """
    # Retrieve the project; raise KeyError if it does not exist
    project = PROJECTS_DB[project_key]

    # Authorization check (CWE-863 mitigation)
    if not _is_authorized(member_id, role, project):
        raise UnauthorizedAccessError(
            f"User '{member_id}' with role '{role}' is not authorized "
            f"to edit settings for project '{project_key}'."
        )

    # Perform a deep copy to avoid accidental mutation of input
    new_settings = copy.deepcopy(updated_configuration)

    # Merge or replace settings (here we simply replace for clarity)
    project["settings"] = new_settings

    return (
        f"Project '{project_key}' settings successfully updated by user "
        f"'{member_id}'."
    )

# --------------------------------------------------------------------------- #
# Example usage (for manual testing)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    try:
        msg = edit_project_settings(
            member_id="user_a",
            role="project_manager",
            project_key="proj_001",
            updated_configuration={"name": "Beta", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")