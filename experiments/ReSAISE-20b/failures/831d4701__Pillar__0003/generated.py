import copy

# Simulated database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": {"user_b", "user_c"},
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Add more projects as needed
}

def update_project_configurations(uid: str, role: str, pid: str, settings: dict) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user ('project_manager', 'team_member', 'viewer', etc.).
    pid : str
        Identifier of the project being modified.
    settings : dict
        New configuration values to apply.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the specified project ID is not found in PROJECTS_DB.
    ValueError
        If the settings argument is not a dictionary.
    """
    # Basic validation of input types
    if not isinstance(settings, dict):
        raise ValueError("settings must be a dictionary")

    # Retrieve the project from the database
    try:
        project = PROJECTS_DB[pid]
    except KeyError as exc:
        raise KeyError(f"Project ID '{pid}' does not exist") from exc

    # Authorization logic
    is_creator = uid == project.get("creator_id")
    is_manager_role = role.lower() == "project_manager"
    # A project manager (role) or the creator can update settings
    if not (is_creator or is_manager_role):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Merge the new settings into the existing configuration
    # We perform a shallow merge to avoid accidental overwrites of nested structures.
    updated_settings = copy.deepcopy(project.get("settings", {}))
    updated_settings.update(settings)

    # Persist the changes back to the database
    project["settings"] = updated_settings

    return f"Project '{pid}' settings successfully updated by user '{uid}'."

# Example usage (for testing purposes)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            uid="user_a",
            role="project_manager",
            pid="proj_001",
            settings={"visibility": "public", "priority": "high"}
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")