# -*- coding: utf-8 -*-
"""
Project configuration updater for a shared project management system.
"""

from __future__ import annotations
import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed.
}

def change_project_config(uid: str, role: str, proj: str, settings_update: Dict[str, Any]) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project whose settings should be changed.
    settings_update : dict
        Dictionary containing the updated settings for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    PermissionError
        If the user is not authorized to modify the project settings.
    """
    # Validate that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Authorization logic:
    #   - Creator can always modify
    #   - Project manager can modify if they are a member
    #   - Team members and viewers cannot modify
    authorized = False
    if uid == project["creator_id"]:
        authorized = True
    elif role.lower() == "project_manager" and uid in project.get("members", []):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform the update (deep copy to avoid side effects)
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(settings_update)

    # Simple validation: ensure settings keys are strings
    if not all(isinstance(k, str) for k in new_settings):
        raise ValueError("All setting keys must be strings.")

    # Update the project's settings
    project["settings"] = new_settings

    return f"Project '{proj}' settings updated successfully."

# Example usage (uncomment to test):
# try:
#     msg = change_project_config("user_123", "project_manager", "proj_001",
#                                 {"visibility": "public"})
#     print(msg)
# except Exception as e:
#     print(e)