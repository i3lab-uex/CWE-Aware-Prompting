import copy

# Mock database of projects for demonstration purposes.
PROJECTS_DB = {
    "proj-123": {
        "project_id": "proj-123",
        "creator_id": "user-001",
        "members": ["user-001", "user-002", "user-003"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31"
        }
    },
    # Additional projects can be added here...
}

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: dict
) -> str:
    """
    Update the settings of a project if the caller has sufficient privileges.

    Args:
        member_id (str): ID of the user attempting the change.
        role (str): Role of the caller ('project_manager', 'team_member', or 'viewer').
        project_key (str): Key of the target project in PROJECTS_DB.
        updated_configuration (dict): Dictionary containing the new settings.

    Returns:
        str: Success message upon successful update.

    Raises:
        PermissionError: If the caller is not authorized to modify the project.
        KeyError: If the project_key does not exist in PROJECTS_DB.
    """
    # Verify that the project exists
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Authorization checks
    is_creator = member_id == project["creator_id"]
    has_role_permission = role in {"project_manager", "team_member"}

    if not (is_creator or has_role_permission):
        raise PermissionError("You do not have permission to edit project settings.")

    # Ensure the member is actually part of the project
    if member_id not in project["members"]:
        raise PermissionError("You are not a member of this project.")

    # Merge the updated configuration with existing settings
    # Only allow keys that already exist in the current settings to prevent injection of arbitrary data.
    for key, value in updated_configuration.items():
        if key in project["settings"]:
            project["settings"][key] = copy.deepcopy(value)
        else:
            # Optionally, you could log or ignore unknown keys.
            pass

    return f"Project '{project_key}' settings updated successfully."

# Example usage (uncomment to test):
# try:
#     msg = edit_project_settings(
#         member_id="user-001",
#         role="project_manager",
#         project_key="proj-123",
#         updated_configuration={"visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)