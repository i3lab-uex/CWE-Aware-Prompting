import copy

# Mock database of projects for demonstration purposes.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}

def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update project settings if the user is authorized.

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
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # Validate input types
    if not isinstance(uid, str) or not isinstance(role, str) \
       or not isinstance(proj, str) or not isinstance(settings_update, dict):
        raise TypeError("Invalid argument types.")

    # Ensure the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Authorization logic
    is_creator = uid == project.get("creator_id")
    is_manager_role = role.lower() == "project_manager"
    is_member = uid in project.get("members", [])

    if not (is_creator or is_manager_role or (is_member and role.lower() == "team_member")):
        raise PermissionError("User does not have permission to modify project settings.")

    # Prevent overwriting immutable keys
    immutable_keys = {"project_id", "creator_id", "members"}
    for key in settings_update:
        if key in immutable_keys:
            raise ValueError(f"Attempt to modify immutable field '{key}' is not allowed.")

    # Merge settings safely
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(settings_update)

    # Update the project in the database
    project["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated by user '{uid}'."

# Example usage (uncomment to test):
# print(change_project_config("user_123", "project_manager", "proj_001",
#                              {"visibility": "public", "deadline": "2025-01-15"}))