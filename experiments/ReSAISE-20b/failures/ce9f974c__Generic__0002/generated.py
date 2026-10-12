import datetime
from typing import Dict, Any

# Mock database of projects (for demonstration purposes)
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
        "last_updated": None,
    },
    # Add more projects as needed
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user has sufficient permissions.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to update settings.
    access_level : str
        Role of the user. Allowed values: 'project_manager', 'team_member', 'viewer'.
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing new configuration values for the project's settings.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    ValueError
        If modifications contain keys that are not allowed to be changed.
    """

    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Define allowed roles to modify settings
    ALLOWED_ROLES = {"project_manager"}

    # Check permissions: either the creator or a project manager
    has_permission = (
        owner_id == project["creator_id"] or access_level in ALLOWED_ROLES
    )

    if not has_permission:
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to modify project settings."
        )

    # Define which keys in settings are allowed to be modified
    ALLOWED_SETTINGS_KEYS = {"deadline", "visibility", "description"}

    # Validate modifications keys
    for key in modifications:
        if key not in ALLOWED_SETTINGS_KEYS:
            raise ValueError(f"Modification of setting '{key}' is not allowed.")

    # Perform the update
    project["settings"].update(modifications)
    project["last_updated"] = datetime.datetime.utcnow().isoformat()

    return f"Project '{proj_id}' settings updated successfully by user '{owner_id}'."