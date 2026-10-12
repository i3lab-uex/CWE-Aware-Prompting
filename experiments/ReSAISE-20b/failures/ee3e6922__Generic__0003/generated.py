from __future__ import annotations

import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_alice",
        "members": ["user_bob", "user_charlie"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here.
}


def change_project_config(uid: str, role: str, proj: str, settings_update: Dict[str, Any]) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting to modify the project.
    role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project to be updated.
    settings_update : dict
        Dictionary containing new or overridden settings for the project.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in `PROJECTS_DB`.
    ValueError
        If `settings_update` contains keys that are not allowed to be changed.
    """
    # Validate project existence
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Authorization: only the creator or a project_manager can modify settings
    if uid != project["creator_id"] and role.lower() != "project_manager":
        raise PermissionError("You do not have permission to modify this project's settings.")

    # Define allowed keys that can be updated. This prevents arbitrary injection.
    ALLOWED_KEYS = {"deadline", "visibility", "name", "description"}

    # Ensure the update only contains allowed keys
    if not set(settings_update).issubset(ALLOWED_KEYS):
        invalid_keys = set(settings_update) - ALLOWED_KEYS
        raise ValueError(f"Attempted to update disallowed settings keys: {invalid_keys}")

    # Deep copy to avoid mutating input
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(settings_update)

    # Persist the changes
    project["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated."


# Example usage (for testing purposes only)
if __name__ == "__main__":
    try:
        msg = change_project_config(
            uid="user_alice",
            role="project_manager",
            proj="proj_001",
            settings_update={"deadline": "2025-01-15", "visibility": "public"},
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")