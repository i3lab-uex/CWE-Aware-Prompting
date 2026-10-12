from __future__ import annotations

import copy
from typing import Dict, Any

# Mock database of projects. In a real application this would be replaced by
# persistent storage (e.g., a database).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"deadline": "2025-01-01", "visibility": "private"},
    },
    # Additional projects can be added here...
}


def change_project_config(
    uid: str, role: str, proj: str, settings_update: Dict[str, Any]
) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        The unique identifier of the user attempting to modify the project.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj : str
        Identifier of the project whose settings should be updated.
    settings_update : dict
        Dictionary containing new or updated setting values.

    Returns
    -------
    str
        Success message indicating the project was updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in the database.
    """

    # Validate that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Authorization logic
    is_creator = uid == project["creator_id"]
    is_manager_role = role.lower() == "project_manager"
    # A project manager can modify any project; a creator can also modify their own.
    if not (is_creator or is_manager_role):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform a deep copy of the existing settings to avoid mutating shared objects
    updated_settings = copy.deepcopy(project["settings"])
    # Merge the new settings; new keys are added, existing keys are overwritten
    updated_settings.update(settings_update)

    # Update the project's settings in place
    project["settings"] = updated_settings

    return f"Project '{proj}' settings updated successfully."