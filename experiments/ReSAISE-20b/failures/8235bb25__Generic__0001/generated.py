import copy

# Example in-memory projects database
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_100",
        "members": ["user_101", "user_102"],
        "settings": {
            "visibility": "private",
            "deadline": "2025-12-31",
        },
    },
    # more projects can be added here
}


def _is_authorized(u_id: str, u_role: str, project: dict) -> bool:
    """
    Determines whether the user is allowed to modify the project's settings.

    * The creator of the project always has permission.
    * Users with role 'project_manager' are allowed to modify any project.
    * Users who are members of the project and have role 'team_member' may also modify settings.
    """
    if u_id == project["creator_id"]:
        return True
    if u_role == "project_manager":
        return True
    if u_role == "team_member" and u_id in project.get("members", []):
        return True
    return False


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: dict,
) -> str:
    """
    Update the configuration settings for a project.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to update.
    modified_settings : dict
        Dictionary containing the settings to be updated.

    Returns
    -------
    str
        Success message if update was performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in ``PROJECTS_DB``.
    ValueError
        If ``modified_settings`` contains keys that are not valid settings for the project.
    """
    # Validate existence of the project
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization check
    if not _is_authorized(u_id, u_role, project):
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    # Ensure that modified_settings keys are valid
    if not isinstance(modified_settings, dict):
        raise ValueError("modified_settings must be a dictionary.")
    valid_keys = set(project.get("settings", {}).keys())
    invalid_keys = set(modified_settings.keys()) - valid_keys
    if invalid_keys:
        raise ValueError(f"Invalid setting keys: {invalid_keys}")

    # Perform a shallow merge of the settings
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(modified_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."