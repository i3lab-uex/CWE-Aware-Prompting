import copy

# Mock database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31"
        }
    },
    # Additional projects can be added here.
}

def update_project_configurations(u_id: str, u_role: str,
                                  proj_id: str, modified_settings: dict) -> str:
    """
    Update the configuration settings of a project.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify settings.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    modified_settings : dict
        Dictionary containing the settings that should be updated.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If the specified project ID is not found in PROJECTS_DB.
    """
    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Determine if the user has permission to modify settings.
    # The creator and users with role 'project_manager' are allowed.
    has_permission = (
        u_id == project["creator_id"] or
        (u_role.lower() == "project_manager" and u_id in project.get("members", []))
    )

    if not has_permission:
        raise PermissionError(
            f"User '{u_id}' does not have permission to modify project '{proj_id}'."
        )

    # Perform a safe update: merge existing settings with the new ones.
    updated_settings = copy.deepcopy(project.get("settings", {}))
    updated_settings.update(modified_settings)

    # Commit the update to the database.
    project["settings"] = updated_settings

    return f"Settings updated successfully for project '{proj_id}'."