from typing import Dict, Any

# Mock database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed.
}

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    project_key : str
        Identifier of the project to modify.
    updated_configuration : dict
        The new settings to apply.

    Returns
    -------
    str
        Success message on successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the project_key is not found in PROJECTS_DB.
    """

    # Ensure the project exists
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Determine authorization: must be the creator or a project_manager
    is_creator = member_id == project["creator_id"]
    is_project_manager = role.lower() == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized to edit project settings."
        )

    # Merge updated configuration into existing settings
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary.")

    project_settings = project.get("settings", {})
    # Perform a shallow merge; nested dicts are replaced entirely.
    project_settings.update(updated_configuration)
    project["settings"] = project_settings

    return f"Project '{project_key}' settings updated successfully."