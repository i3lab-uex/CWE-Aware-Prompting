import copy

# Sample in‑memory database of projects
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        # Default settings
        "settings": {
            "visibility": "private",
            "notifications": True,
            "deadline": None
        }
    },
    # Add more projects as needed...
}

def _is_authorized(member_id: str, member_role: str, project: dict) -> bool:
    """
    Internal helper that determines whether a user is allowed to modify the
    project's settings.
    
    A user can modify the settings if:
        1. The user is the creator of the project, or
        2. The user has a 'project_manager' role and is listed as a member.
    """
    if member_id == project["creator_id"]:
        return True
    if member_role == "project_manager" and member_id in project["members"]:
        return True
    return False

def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: dict
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the settings.
    member_role : str
        Role of the user ('project_manager', 'team_member', etc.).
    proj_id : str
        ID of the target project.
    fresh_settings : dict
        Dictionary containing key/value pairs to update in the project's settings.

    Returns
    -------
    str
        Success message when the settings are updated.

    Raises
    ------
    PermissionError
        If the caller does not have permission to modify the project settings.
    KeyError
        If the project ID is unknown.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization check (CWE-863 mitigation)
    if not _is_authorized(member_id, member_role, project):
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized to modify project settings."
        )

    # Perform a safe deep copy of the current settings
    updated_settings = copy.deepcopy(project["settings"])

    # Validate that fresh_settings is a dict
    if not isinstance(fresh_settings, dict):
        raise ValueError("fresh_settings must be a dictionary.")

    # Update settings; only keys that already exist are allowed to prevent
    # accidental injection of new, unexpected configuration.
    for key, value in fresh_settings.items():
        if key not in updated_settings:
            raise KeyError(f"Setting '{key}' is not a valid project setting.")
        updated_settings[key] = value

    # Commit the changes
    project["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated."

# Example usage (uncomment to test)
# try:
#     msg = alter_project_preferences(
#         member_id="user_456",
#         member_role="project_manager",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public", "deadline": "2025-12-31"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)