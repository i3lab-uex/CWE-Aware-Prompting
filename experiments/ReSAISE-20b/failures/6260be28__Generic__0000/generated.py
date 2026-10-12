# Dictionary simulating a simple project database.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}

def modify_project_settings(user_id: str, user_role: str,
                            project_id: str, new_settings: dict) -> str:
    """
    Update the settings of a project after performing authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        The role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        The ID of the project being modified.
    new_settings : dict
        Dictionary containing the new settings to apply.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    ValueError
        If the project does not exist.
    PermissionError
        If the user is not authorized to modify settings.

    Notes
    -----
    - Only a project manager or the creator can change settings.
    - `new_settings` must be a dictionary; other types are rejected.
    """
    # Ensure the project exists
    if project_id not in PROJECTS_DB:
        raise ValueError(f"Project '{project_id}' does not exist.")

    project = PROJECTS_DB[project_id]

    # Authorization: Only project managers or the creator can modify settings
    if user_role != "project_manager" and user_id != project["creator_id"]:
        raise PermissionError("User is not authorized to modify project settings.")

    # Validate that new_settings is a dictionary
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary.")

    # Merge the new settings into existing ones
    project["settings"].update(new_settings)

    return (
        f"Project '{project_id}' settings successfully updated by user "
        f"'{user_id}'."
    )