import copy

# Sample in‑memory database for demonstration purposes.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # ... more projects
}

def edit_project_settings(member_id: str, role: str, project_key: str,
                          updated_configuration: dict) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        The role of the user. Expected values: 'project_manager',
        'team_member', or 'viewer'.
    project_key : str
        The identifier of the project whose settings should be changed.
    updated_configuration : dict
        The new configuration values to merge into the existing settings.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user does not have permission to edit project settings.
    KeyError
        If the specified project_key is not found in PROJECTS_DB.
    """
    # Validate that the project exists
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Authorization logic:
    # 1. The creator can always edit.
    # 2. A project_manager member can also edit.
    # 3. Other roles are not permitted to modify settings.
    authorized = False
    if member_id == project["creator_id"]:
        authorized = True
    elif role.lower() == "project_manager" and member_id in project["members"]:
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{role}' is not authorized to edit project settings."
        )

    # Merge the updated configuration into existing settings.
    # We use a shallow copy to avoid accidental mutation of the original dict
    new_settings = copy.deepcopy(project["settings"])
    for key, value in updated_configuration.items():
        # Basic validation: ensure keys are expected
        if key not in new_settings:
            raise ValueError(f"Unknown setting '{key}'.")
        # Additional type checks can be added here as needed.
        new_settings[key] = value

    project["settings"] = new_settings
    return f"Project '{project_key}' settings updated successfully."

# Example usage (uncomment to test):
# try:
#     msg = edit_project_settings(
#         member_id="user_123",
#         role="project_manager",
#         project_key="proj_001",
#         updated_configuration={"visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)