import copy

# Mock database of projects for demonstration purposes.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {"name": "Alpha", "deadline": "2024-12-31"},
    },
    "proj_002": {
        "project_id": "proj_002",
        "creator_id": "user_b",
        "members": ["user_a"],
        "settings": {"name": "Beta", "deadline": "2025-01-15"},
    },
}


def change_project_config(uid: str, role: str, proj: str, settings_update: dict) -> str:
    """
    Update the configuration of a project if the user is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    proj : str
        Identifier of the project whose settings should be changed.
    settings_update : dict
        Dictionary containing the updated settings for the project.

    Returns
    -------
    str
        Success message indicating that the project settings were updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in the database.
    """
    # Verify that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Determine if the user has permission
    is_creator = uid == project["creator_id"]
    is_manager = role.lower() == "project_manager"

    # Authorization logic: project managers can edit any project; otherwise
    # only the creator may edit. Team members and viewers cannot edit.
    if not (is_manager or is_creator):
        raise PermissionError(
            f"User '{uid}' with role '{role}' does not have permission "
            "to modify project settings."
        )

    # Perform a deep copy to avoid accidental mutation of the input
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(settings_update)

    # Update the project settings in place
    PROJECTS_DB[proj]["settings"] = new_settings

    return f"Project '{proj}' settings updated successfully."


# Example usage
if __name__ == "__main__":
    try:
        msg = change_project_config(
            uid="user_a",
            role="project_manager",
            proj="proj_001",
            settings_update={"deadline": "2025-06-30", "budget": 10000},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")