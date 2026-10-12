import uuid
from typing import Dict, Any

# Mock database of projects for demonstration purposes.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-123": {
        "project_id": "proj-123",
        "creator_id": "user-001",
        "members": ["user-002", "user-003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here.
}

# Define which access levels are allowed to modify project settings
ALLOWED_ROLES = {"project_manager", "creator"}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update project settings if the user has sufficient rights.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to update settings.
    access_level : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing new configuration values for the project.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # 1. Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Determine if the user is authorized
    is_creator = owner_id == project["creator_id"]
    has_manager_role = access_level in ALLOWED_ROLES

    # Authorization check must be performed *after* retrieving the project
    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to modify project '{proj_id}'."
        )

    # 3. Apply modifications safely
    for key, value in modifications.items():
        if key not in project["settings"]:
            # Optionally allow adding new settings or reject unknown keys
            raise KeyError(f"Setting '{key}' is not a valid project setting.")
        project["settings"][key] = value

    # 4. Return success message
    return f"Project '{proj_id}' settings updated successfully by user '{owner_id}'."