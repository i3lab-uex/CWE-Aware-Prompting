import copy

# Sample in‑memory projects database
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "notifications": True,
        },
    },
    # Add more projects as needed
}

# Roles that are allowed to alter project settings
ALLOWED_ROLES = {"project_manager", "team_leader"}


def alter_project_preferences(member_id: str,
                               member_role: str,
                               proj_id: str,
                               fresh_settings: dict) -> str:
    """
    Modify the settings of a project if the user has sufficient privileges.

    Args:
        member_id: ID of the requesting user.
        member_role: Role of the requesting user
                     (e.g., 'project_manager', 'team_member', 'viewer').
        proj_id: ID of the project to be updated.
        fresh_settings: Dictionary containing new settings.

    Returns:
        Success message if the update is performed.

    Raises:
        PermissionError: If the user is not authorized to modify settings.
        KeyError: If the project ID does not exist.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: allow if user is creator or has an allowed role
    authorized = (
        member_id == project["creator_id"] or
        member_role in ALLOWED_ROLES
    )

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized "
            "to modify project settings."
        )

    # Ensure that fresh_settings only contains keys that are allowed to be changed
    # (example: restrict certain sensitive settings)
    ALLOWED_SETTING_KEYS = {"visibility", "notifications"}
    for key in fresh_settings:
        if key not in ALLOWED_SETTING_KEYS:
            raise ValueError(f"Setting '{key}' is not allowed to be modified.")

    # Apply the updates in a safe manner
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(fresh_settings)
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated by user '{member_id}'."