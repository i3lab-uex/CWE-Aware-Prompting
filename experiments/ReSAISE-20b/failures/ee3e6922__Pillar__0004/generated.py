import copy

# Simulated in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"name": "Alpha", "visibility": "private"},
    },
    # ... other projects ...
}

def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project whose settings should be changed.
    settings_update : dict
        Updated key/value pairs for the project's settings.

    Returns
    -------
    str
        Success message if update succeeds.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist.
    ValueError
        If settings_update is not a dictionary.
    """
    # Basic type checks to guard against malformed input
    if not isinstance(settings_update, dict):
        raise ValueError("settings_update must be a dictionary")

    # Retrieve the project from the database
    try:
        project = PROJECTS_DB[proj]
    except KeyError as exc:
        raise KeyError(f"Project '{proj}' not found") from exc

    # Authorization logic
    is_creator = uid == project["creator_id"]
    has_manager_role = role.lower() == "project_manager"
    is_member = uid in project["members"]

    # Only creators, managers or members with explicit permission can edit settings
    if not (is_creator or has_manager_role or is_member):
        raise PermissionError("User does not have permission to modify this project")

    # Merge settings safely (deep copy to avoid side effects)
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(settings_update)

    # Apply the update
    project["settings"] = updated_settings

    return f"Project '{proj}' settings updated successfully."

# Example usage (uncomment to test):
# try:
#     msg = change_project_config("user_b", "team_member", "proj_001",
#                                 {"visibility": "public"})
#     print(msg)
# except Exception as e:
#     print(e)