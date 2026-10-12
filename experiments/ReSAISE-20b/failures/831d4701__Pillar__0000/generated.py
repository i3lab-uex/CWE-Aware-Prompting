import copy

# Example in-memory database of projects
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "userA",
        "members": ["userB", "userC"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # Add more projects as needed
}

def update_project_configurations(uid: str, role: str, pid: str, settings: dict) -> str:
    """
    Update the configuration of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update.
    role : str
        Role of the user ('project_manager', 'team_member', 'viewer', etc.).
    pid : str
        Identifier of the project to be modified.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    """
    # Validate that the project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project ID '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Authorization logic
    is_creator = uid == project["creator_id"]
    is_manager = role.lower() == "project_manager"
    # Optionally, allow members to edit if they are managers
    is_member = uid in project["members"]

    # Only creators or users with the 'project_manager' role can update
    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Ensure settings is a dict and does not contain disallowed keys
    if not isinstance(settings, dict):
        raise ValueError("Settings must be provided as a dictionary.")

    # Optional: whitelist allowed setting keys
    ALLOWED_KEYS = {"visibility", "deadline", "description", "tags"}
    for key in settings:
        if key not in ALLOWED_KEYS:
            raise ValueError(f"Setting '{key}' is not allowed to be updated.")

    # Perform the update safely
    project["settings"].update(copy.deepcopy(settings))

    return f"Project '{pid}' settings updated successfully by user '{uid}'."