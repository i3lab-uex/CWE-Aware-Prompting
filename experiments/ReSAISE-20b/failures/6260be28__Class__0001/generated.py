import copy

# Mock database of projects for demonstration purposes.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Additional projects can be added here.
}

def modify_project_settings(user_id: str, user_role: str,
                            project_id: str, new_settings: dict) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify settings.
    user_role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    project_id : str
        ID of the target project.
    new_settings : dict
        Dictionary containing settings to apply.

    Returns
    -------
    str
        Confirmation message if the update succeeds, or an authorization error.

    Raises
    ------
    ValueError
        If the project_id does not exist in PROJECTS_DB.
    """

    # Validate input types
    if not isinstance(new_settings, dict):
        raise TypeError("new_settings must be a dictionary")

    # Retrieve the project; raise if it does not exist
    project = PROJECTS_DB.get(project_id)
    if project is None:
        raise ValueError(f"Project '{project_id}' does not exist")

    # Authorization logic
    is_creator = user_id == project["creator_id"]
    is_manager = user_role == "project_manager"
    # For extra safety, check if the user is a member of the project
    is_member = user_id in project["members"]

    # Only creators or users with the 'project_manager' role can modify settings.
    # Optionally, allow managers who are also members.
    if not (is_creator or is_manager):
        return f"Authorization error: User '{user_id}' does not have permission to modify project settings."

    # Perform the update (deep copy to avoid accidental mutation)
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(new_settings)

    # Apply the update to the database
    project["settings"] = updated_settings

    return f"Project '{project_id}' settings successfully updated by user '{user_id}'."