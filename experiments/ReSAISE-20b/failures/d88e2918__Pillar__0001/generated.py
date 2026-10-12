import threading

# Simulated in‑memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"title": "Initial Project", "visibility": "private"},
    },
    # Add more projects as needed
}

# Lock to protect concurrent access to PROJECTS_DB
_db_lock = threading.Lock()


def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: dict,
) -> str:
    """
    Update the settings of a project if the caller has sufficient privileges.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        Role of the caller, e.g., 'project_manager', 'team_member', or 'viewer'.
    project_key : str
        Identifier of the project to update.
    updated_configuration : dict
        Dictionary containing the new settings for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the caller is not authorized to modify the project settings.
    KeyError
        If `project_key` does not exist in PROJECTS_DB.
    ValueError
        If `updated_configuration` is not a dictionary.
    """
    # Basic validation of the input configuration
    if not isinstance(updated_configuration, dict):
        raise ValueError("updated_configuration must be a dictionary")

    with _db_lock:
        # Ensure the project exists
        if project_key not in PROJECTS_DB:
            raise KeyError(f"Project {project_key} does not exist")

        project = PROJECTS_DB[project_key]

        # Authorization check:
        # - The creator can edit any settings.
        # - A user with role 'project_manager' and who is a member can edit.
        authorized = False
        if member_id == project["creator_id"]:
            authorized = True
        elif role == "project_manager" and member_id in project["members"]:
            authorized = True

        if not authorized:
            raise PermissionError(
                f"User {member_id} with role '{role}' is not authorized to edit project settings"
            )

        # Perform the update
        project["settings"].update(updated_configuration)

    return f"Project {project_key} settings updated successfully."


# Example usage (uncomment to test):
# try:
#     msg = edit_project_settings(
#         member_id="user_123",
#         role="project_manager",
#         project_key="proj_001",
#         updated_configuration={"visibility": "public", "deadline": "2024-12-31"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)