from typing import Dict, Any

# Sample in-memory projects database
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict[str, Any],
) -> str:
    """
    Update project settings if the user has proper authorization.

    Args:
        u_id (str): ID of the user attempting to update.
        u_role (str): Role of the user. Accepted values: 'project_manager', 'team_member'.
        proj_id (str): ID of the project to update.
        modified_settings (dict): New settings values.

    Returns:
        str: Success message upon successful update.

    Raises:
        PermissionError: If the user is not authorized to modify the project.
        KeyError: If the project ID does not exist in PROJECTS_DB.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    is_creator = u_id == project["creator_id"]
    is_member = u_id in project.get("members", [])
    has_permission = False

    if u_role == "project_manager":
        # Project managers can update any project they own or are a member of
        has_permission = is_creator or is_member
    elif u_role == "team_member":
        # Team members can only update projects they are part of
        has_permission = is_member

    if not has_permission:
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to update project '{proj_id}'."
        )

    # Update settings safely
    for key, value in modified_settings.items():
        project["settings"][key] = value

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test):
# try:
#     msg = update_project_configurations(
#         u_id="user456",
#         u_role="team_member",
#         proj_id="proj1",
#         modified_settings={"visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)