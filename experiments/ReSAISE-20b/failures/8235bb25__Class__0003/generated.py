#!/usr/bin/env python3
"""
A minimal implementation of a project configuration updater for a shared
project management platform.  The function ensures that only users with the
appropriate permissions can modify project settings.

Author: OpenAI ChatGPT
"""

from __future__ import annotations

import copy
from typing import Dict, Any

# Sample in-memory database of projects. In a real application this would be
# replaced by persistent storage such as a relational database or an ORM.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # ... other projects ...
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict[str, Any],
) -> str:
    """
    Update the configuration settings of a project.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to be updated.
    modified_settings : dict
        Dictionary containing key/value pairs to update in the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If the specified project ID is not found in the database.
    ValueError
        If `modified_settings` contains keys that are not allowed to be modified.

    Notes
    -----
    The function performs a strict authorization check:
      * The user must be the creator of the project.
      * OR the user must have a role that is explicitly allowed to modify
        settings (currently only 'project_manager').
    This prevents CWE-863: Incorrect Authorization.
    """
    # --- Retrieve project ---
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' does not exist.") from exc

    # --- Authorization check ---
    authorized_roles = {"project_manager"}
    is_creator = u_id == project["creator_id"]
    has_role_permission = u_role in authorized_roles

    if not (is_creator or has_role_permission):
        raise PermissionError(
            "You do not have permission to modify this project's settings."
        )

    # --- Validate modified_settings keys ---
    # Only allow a whitelist of settings to be updated.
    allowed_keys = {"visibility", "deadline", "description"}
    for key in modified_settings:
        if key not in allowed_keys:
            raise ValueError(f"Setting '{key}' cannot be modified.")

    # --- Apply updates ---
    # Use a copy to avoid accidental mutation of the original dict during
    # validation (defensive programming).
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(modified_settings)

    # Commit changes back to the "database"
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            u_id="user_123",
            u_role="viewer",
            proj_id="proj_001",
            modified_settings={"visibility": "public"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")