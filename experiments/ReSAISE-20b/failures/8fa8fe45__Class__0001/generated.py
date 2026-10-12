import copy

# Sample in-memory database of projects.
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

def alter_project_preferences(member_id: str,
                               member_role: str,
                               proj_id: str,
                               fresh_settings: dict) -> str:
    """
    Modify the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the project.
    member_role : str
        Role of the user ('project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    fresh_settings : dict
        Dictionary containing the new settings.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the project ID is not found in the database.
    ValueError
        If `fresh_settings` is not a dictionary.
    """
    # Validate input types
    if not isinstance(fresh_settings, dict):
        raise ValueError("fresh_settings must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as e:
        raise KeyError(f"Project '{proj_id}' not found") from e

    # Authorization logic
    is_creator = member_id == project["creator_id"]
    is_manager = member_role.lower() == "project_manager"
    is_member = member_id in project.get("members", [])

    # Only the creator or a user with the 'project_manager' role can modify settings.
    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' "
            "is not authorized to modify project settings."
        )

    # Optional: Ensure that the user is a member if they are not the creator.
    if not is_creator and not is_member:
        raise PermissionError(
            f"User '{member_id}' is not a member of project '{proj_id}'."
        )

    # Perform the update
    updated_settings = copy.deepcopy(project.get("settings", {}))
    updated_settings.update(fresh_settings)
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated by user '{member_id}'."