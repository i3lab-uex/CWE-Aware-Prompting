import copy
from typing import Dict, Any

# Mock database of projects. In a real application this would be replaced by
# persistent storage (e.g., a database).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_123", "user_456"},
        "settings": {
            "name": "Website Redesign",
            "deadline": "2024-12-31",
            "visibility": "private"
        }
    },
    # Additional projects can be added here
}

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict[str, Any]
) -> str:
    """
    Update the settings of a project.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting to modify settings.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_key : str
        Identifier of the project whose settings should be updated.
    updated_configuration : dict
        Dictionary containing the new configuration values.

    Returns
    -------
    str
        Success message indicating that settings were updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in the database.
    ValueError
        If `updated_configuration` is not a dictionary or contains invalid keys.
    """
    # Verify that the project exists
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Authorization logic:
    #   • The creator of the project can always edit settings.
    #   • A user with role 'project_manager' can also edit, regardless of membership.
    #   • All other roles are forbidden from editing settings.
    is_creator = member_id == project["creator_id"]
    is_manager = role.lower() == "project_manager"

    if not (is_creator or is_manager):
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit settings for project '{project_key}'."
        )

    # Basic validation of the updated configuration
    if not isinstance(updated_configuration, dict):
        raise ValueError("Updated configuration must be a dictionary.")

    # Optionally restrict allowed keys to prevent tampering with protected fields
    allowed_keys = {"name", "deadline", "visibility"}
    for key in updated_configuration:
        if key not in allowed_keys:
            raise ValueError(f"Setting '{key}' is not allowed to be updated.")

    # Perform the update safely by creating a copy of the current settings
    new_settings = copy.deepcopy(project["settings"])
    new_settings.update(updated_configuration)

    # Persist the changes back to the mock database
    project["settings"] = new_settings

    return (
        f"Project '{project_key}' settings updated successfully by user '{member_id}'."
    )

# Example usage (uncomment to test):
# try:
#     msg = edit_project_settings(
#         member_id="user_123",
#         role="project_manager",
#         project_key="proj_001",
#         updated_configuration={"visibility": "public", "deadline": "2025-01-15"}
#     )
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")