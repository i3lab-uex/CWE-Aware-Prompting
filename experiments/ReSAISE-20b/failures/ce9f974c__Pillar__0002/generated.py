# -*- coding: utf-8 -*-
"""
Project management utilities.
"""

from typing import Dict, Any

# Sample in-memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "name": "Website Redesign",
            "visibility": "private",
        },
    },
    # ... additional projects ...
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update project settings if the caller has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify settings.
    access_level : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the target project.
    modifications : dict
        Key/value pairs with new configuration for the project's settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    ValueError
        If modifications contain invalid keys for the settings dictionary.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The creator always has full rights.
    # 2. A project manager (access_level) also has rights.
    # 3. Other roles are denied modification access.
    authorized = False
    if owner_id == project["creator_id"]:
        authorized = True
    elif access_level.lower() == "project_manager":
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' "
            "is not authorized to change project settings."
        )

    # Validate that modifications only target existing setting keys
    current_settings = project.get("settings", {})
    invalid_keys = set(modifications) - set(current_settings)
    if invalid_keys:
        raise ValueError(
            f"Attempted to modify unknown setting keys: {sorted(invalid_keys)}"
        )

    # Apply modifications atomically
    project["settings"].update(modifications)

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = change_project_settings(
#             owner_id="user_123",
#             access_level="project_manager",
#             proj_id="proj_001",
#             modifications={"visibility": "public"},
#         )
#         print(msg)
#     except Exception as e:
#         print(e)