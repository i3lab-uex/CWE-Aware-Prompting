import typing

# Sample in‑memory database of projects.
# In a real system this would be replaced with persistent storage.
PROJECTS_DB: dict[str, dict] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # ... other projects ...
}


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: typing.Dict[str, typing.Any],
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Args:
        member_id: ID of the user making the request.
        role: Role of the caller. Accepted values are
              'project_manager', 'team_member', or 'viewer'.
        project_key: Identifier of the target project.
        updated_configuration: Dictionary containing new settings.

    Returns:
        Success message string.

    Raises:
        PermissionError: If the caller is not authorized to modify the project.
        KeyError: If the specified project does not exist.
    """
    # Validate role input to avoid injection or unexpected values
    valid_roles = {"project_manager", "team_member", "viewer"}
    if role not in valid_roles:
        raise ValueError(f"Invalid role: {role!r}")

    # Retrieve the project; KeyError if not found
    project = PROJECTS_DB[project_key]

    # Authorization check:
    # Only the creator or a project_manager may modify settings.
    is_creator = member_id == project["creator_id"]
    is_project_manager = role == "project_manager"

    if not (is_creator or is_project_manager):
        raise PermissionError(
            f"User {member_id!r} with role {role!r} is not authorized "
            f"to edit settings for project {project_key!r}"
        )

    # Perform the update atomically
    project_settings = project.setdefault("settings", {})
    for key, value in updated_configuration.items():
        # Basic type checks can be added here as needed
        project_settings[key] = value

    return f"Project {project_key!r} settings updated successfully."