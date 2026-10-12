from typing import Dict

# Sample in-memory database of projects.
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # Additional projects can be added here.
}


def update_project_configurations(
    uid: str, role: str, pid: str, settings: Dict
) -> str:
    """
    Update the configuration of a project if the user has sufficient rights.

    Args:
        uid (str): The identifier representing the user attempting to update settings.
        role (str): Describing the user's role (e.g., 'project_manager', 'team_member', 'viewer').
        pid (str): The identifier of the project being modified.
        settings (dict): New configuration for the project.

    Returns:
        str: Success message indicating that the settings have been updated.

    Raises:
        PermissionError: If the user is not authorized to modify the project.
        KeyError: If the project does not exist in PROJECTS_DB.
    """
    # Retrieve the project, raising KeyError if it doesn't exist.
    project = PROJECTS_DB[pid]

    # Authorization logic:
    # - The creator of the project always has permission.
    # - A user with role 'project_manager' and who is a member of the project has permission.
    # - Other roles (e.g., 'team_member', 'viewer') are not permitted to update settings.
    is_creator = uid == project["creator_id"]
    is_member = uid in project.get("members", [])
    has_manager_role = role == "project_manager"

    if not (is_creator or (has_manager_role and is_member)):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Update the project's settings. We merge the existing settings with the new ones.
    project["settings"].update(settings)

    return f"Project '{pid}' settings updated successfully by user '{uid}'."