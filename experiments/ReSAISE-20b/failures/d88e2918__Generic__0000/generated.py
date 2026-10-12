import copy

# Example in-memory database of projects
PROJECTS_DB = {
    # project_id: {project_id, creator_id, members (list of ids), settings (dict)}
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: dict,
) -> str:
    """
    Update settings of a project if the caller has sufficient permissions.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_key : str
        The identifier of the project whose settings should be changed.
    updated_configuration : dict
        Updated configuration values to apply.

    Returns
    -------
    str
        Success message if the update is performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If the specified project key does not exist in `PROJECTS_DB`.
    ValueError
        If updated_configuration is not a dictionary.
    """
    # Validate input types
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[project_key]
    except KeyError as exc:
        raise KeyError(f"Project '{project_key}' not found") from exc

    # Permission check: only project manager or creator can modify settings
    is_creator = member_id == project["creator_id"]
    is_manager = role.lower() == "project_manager"
    if not (is_creator or is_manager):
        raise PermissionError("You do not have permission to edit project settings")

    # Optional: ensure member is part of the project
    if member_id not in project["members"]:
        raise PermissionError("User is not a member of this project")

    # Merge new settings with existing ones (shallow merge)
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(updated_configuration)

    # Update the project settings
    project["settings"] = updated_settings

    return f"Project '{project_key}' settings successfully updated."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         msg = edit_project_settings(
#             member_id="user-123",
#             role="project_manager",
#             project_key="proj-001",
#             updated_configuration={"visibility": "public", "budget": 50000},
#         )
#         print(msg)
#     except Exception as e:
#         print(f"Error: {e}")