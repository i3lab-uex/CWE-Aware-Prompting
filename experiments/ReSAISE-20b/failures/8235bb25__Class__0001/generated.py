import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed.
}

def update_project_configurations(u_id: str, u_role: str, proj_id: str, modified_settings: dict) -> str:
    """
    Update project settings if the user is authorized.

    Args:
        u_id (str): ID of the user attempting to modify settings.
        u_role (str): Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
        proj_id (str): ID of the project to update.
        modified_settings (dict): Dictionary containing settings to be updated.

    Returns:
        str: Success message upon successful update.

    Raises:
        PermissionError: If the user is not authorized to modify project settings.
        KeyError: If the specified project does not exist.
    """
    # Retrieve the target project
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The creator can always modify.
    # 2. Users with role 'project_manager' can modify if they are a member of the project.
    # 3. No other roles are permitted to modify settings.
    is_creator = u_id == project["creator_id"]
    is_manager_and_member = (u_role == "project_manager" and u_id in project["members"])

    if not (is_creator or is_manager_and_member):
        raise PermissionError("You do not have permission to modify this project's settings.")

    # Perform the update (deep copy to avoid accidental mutation of input)
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(copy.deepcopy(modified_settings))

    # Commit the changes
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."