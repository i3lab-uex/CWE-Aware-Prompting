import copy

# Example in-memory projects database (replace with real persistence in production)
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user456", "user789"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}

def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update project configuration if the user is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project whose settings should be changed.
    settings_update : dict
        Updated settings for the project.

    Returns
    -------
    str
        Success message indicating that the project settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    """
    # Validate input types
    if not isinstance(uid, str) or not isinstance(role, str) \
       or not isinstance(proj, str) or not isinstance(settings_update, dict):
        raise TypeError("Invalid argument types provided.")

    # Retrieve the project; raise KeyError if not found
    project = PROJECTS_DB.get(proj)
    if project is None:
        raise KeyError(f"Project with ID '{proj}' does not exist.")

    # Authorization check: only creator or project_manager can modify settings
    if uid != project.get("creator_id") and role.lower() != "project_manager":
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Perform a deep copy of the existing settings to avoid accidental mutation
    current_settings = copy.deepcopy(project.get("settings", {}))

    # Merge updates into the existing settings
    updated_settings = {**current_settings, **settings_update}

    # Validate that the updated settings are a dict and contain no prohibited keys
    if not isinstance(updated_settings, dict):
        raise ValueError("Updated settings must be a dictionary.")

    # Optionally: restrict certain keys from being updated
    prohibited_keys = {"project_id", "creator_id", "members"}
    if any(key in prohibited_keys for key in updated_settings):
        raise ValueError(f"Attempt to modify restricted keys: {prohibited_keys}")

    # Commit the changes
    project["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated by user '{uid}'."