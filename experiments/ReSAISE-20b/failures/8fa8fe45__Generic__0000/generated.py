import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"}
    },
    # Add more projects as needed...
}

def alter_project_preferences(member_id: str,
                               member_role: str,
                               proj_id: str,
                               fresh_settings: dict) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the project.
    member_role : str
        Role of the user in the platform (e.g. 'project_manager',
        'team_member', 'viewer').
    proj_id : str
        ID of the project to update.
    fresh_settings : dict
        New settings that should replace or merge into the existing ones.

    Returns
    -------
    str
        Success message if update is performed, otherwise an error string.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    """
    # Validate that project exists
    if proj_id not in PROJECTS_DB:
        return f"Error: Project '{proj_id}' does not exist."

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    is_creator = member_id == project["creator_id"]
    has_manager_role = member_role == "project_manager"
    is_member = member_id in project["members"]

    # Only creators or users with 'project_manager' role can modify settings.
    if not (is_creator or has_manager_role):
        raise PermissionError(
            f"User '{member_id}' does not have permission to alter project "
            f"settings for project '{proj_id}'."
        )

    # Merge or replace settings safely
    # We deep‑copy to avoid accidental reference sharing.
    new_settings = copy.deepcopy(project.get("settings", {}))
    new_settings.update(fresh_settings)
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."