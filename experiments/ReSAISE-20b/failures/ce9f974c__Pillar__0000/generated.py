import copy

# Simulated database of projects.
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "userA",
        "members": ["userB", "userC"],
        "settings": {"deadline": "2025-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}


def change_project_settings(owner_id: str, access_level: str, proj_id: str,
                            modifications: dict) -> str:
    """
    Update the settings of a project if the caller has sufficient rights.

    Args:
        owner_id (str): Identifier of the user attempting to modify settings.
        access_level (str): Role of the caller ('project_manager', 'team_member',
                            or 'viewer').
        proj_id (str): Identifier of the project to modify.
        modifications (dict): New configuration values for the project's settings.

    Returns:
        str: Success message upon successful update.

    Raises:
        PermissionError: If the caller does not have permission to modify the project.
        KeyError: If the project ID is unknown or required keys are missing.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Determine if the user has permission
    is_creator = owner_id == project["creator_id"]
    is_manager = access_level.lower() == "project_manager"
    has_permission = is_creator or is_manager

    if not has_permission:
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to modify project '{proj_id}'."
        )

    # Merge modifications into existing settings safely
    if not isinstance(modifications, dict):
        raise ValueError("Modifications must be a dictionary.")

    # Optionally validate keys here; for now we accept any key.
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(modifications)

    # Apply the changes
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings have been successfully updated."


# Example usage:
if __name__ == "__main__":
    try:
        msg = change_project_settings(
            owner_id="userA",
            access_level="project_manager",
            proj_id="proj1",
            modifications={"visibility": "public", "deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")