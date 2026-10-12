import copy

# Example in‑memory database of projects.
# Each project is a dict with the following keys:
#   - 'project_id': unique identifier
#   - 'creator_id': user id of the project creator
#   - 'members': list of user ids with at least member access
#   - 'settings': dict containing project configuration
PROJECTS_DB = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-123",
        "members": ["user-123", "user-456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}

# Define which settings keys are allowed to be modified.
ALLOWED_SETTINGS_KEYS = {"deadline", "visibility", "description"}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: dict,
) -> str:
    """
    Update the settings of a project if the caller has sufficient privileges.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify settings.
    access_level : str
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Dictionary containing setting keys and their new values.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the project.
    KeyError
        If the specified project does not exist.
    ValueError
        If modifications contain disallowed keys or invalid values.
    """

    # 1. Retrieve the project from the database
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found.") from exc

    # 2. Verify that the caller has sufficient rights
    # Only a project manager (or creator) may modify settings.
    if access_level != "project_manager":
        raise PermissionError(
            f"User '{owner_id}' with role '{access_level}' is not authorized to change settings."
        )

    # 3. Ensure the caller is either the creator or a member of the project
    if owner_id != project["creator_id"] and owner_id not in project["members"]:
        raise PermissionError(
            f"User '{owner_id}' is not a member of project '{proj_id}'."
        )

    # 4. Validate the modifications dictionary
    if not isinstance(modifications, dict):
        raise ValueError("Modifications must be a dictionary.")

    for key in modifications:
        if key not in ALLOWED_SETTINGS_KEYS:
            raise ValueError(f"Modification key '{key}' is not allowed.")
        # Add any value validation logic here (e.g., date format, enum checks)
        # For simplicity, we skip detailed validation.

    # 5. Apply the modifications atomically
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(modifications)
    project["settings"] = updated_settings

    return (
        f"Project '{proj_id}' settings successfully updated by user '{owner_id}'."
    )