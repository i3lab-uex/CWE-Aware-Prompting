import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    # project_id: project_data
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": [
            {"member_id": "user_123", "role": "project_manager"},
            {"member_id": "user_456", "role": "team_member"},
        ],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # more projects can be added here...
}


def alter_project_preferences(member_id: str,
                               member_role: str,
                               proj_id: str,
                               fresh_settings: dict) -> str:
    """
    Update project settings if the caller has sufficient privileges.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    fresh_settings : dict
        New settings values.

    Returns
    -------
    str
        Success message on successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the project ID does not exist in PROJECTS_DB.
    ValueError
        If fresh_settings is not a dictionary or contains invalid keys.
    """

    # 1. Validate input types
    if not isinstance(fresh_settings, dict):
        raise ValueError("fresh_settings must be a dictionary.")

    # 2. Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project with ID '{proj_id}' not found.") from exc

    # 3. Authorization logic
    is_creator = project["creator_id"] == member_id
    # Find the member record in the project's members list.
    member_record = next(
        (m for m in project["members"] if m["member_id"] == member_id),
        None,
    )

    # A project manager or the creator can modify settings.
    has_permission = (
        is_creator
        or (member_record and member_record["role"] == "project_manager")
    )

    if not has_permission:
        raise PermissionError(
            f"User '{member_id}' does not have permission to modify project '{proj_id}'."
        )

    # 4. Update settings safely (deep copy to avoid mutation side‑effects)
    updated_settings = copy.deepcopy(project["settings"])
    for key, value in fresh_settings.items():
        # Optionally validate keys or types here.
        updated_settings[key] = value

    project["settings"] = updated_settings
    return f"Project '{proj_id}' settings successfully updated."


# Example usage (uncomment to test):
# try:
#     msg = alter_project_preferences(
#         member_id="user_123",
#         member_role="project_manager",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public", "deadline": "2025-01-15"},
#     )
#     print(msg)
# except Exception as e:
#     print(e)