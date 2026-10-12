import copy

# Example in‑memory database of projects.
# Each project is a dict containing:
#   - 'project_id': str
#   - 'creator_id': str
#   - 'members': list[str]  (ids of all users who can view the project)
#   - 'settings': dict      (project configuration settings)
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456", "user_789"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"}
    },
    # Add more projects as needed.
}


def alter_project_preferences(member_id: str,
                               member_role: str,
                               proj_id: str,
                               fresh_settings: dict) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Args:
        member_id (str): ID of the user requesting the change.
        member_role (str): Role of the user in the system.
                           Expected values: 'project_manager', 'team_member', 'viewer'.
        proj_id (str): ID of the project to update.
        fresh_settings (dict): New settings values.

    Returns:
        str: Success message when the update is applied.

    Raises:
        PermissionError: If the user does not have permission to modify the project.
        KeyError: If the project ID is unknown.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization: only the creator or a user with role 'project_manager'
    # and who is listed in the project's members can modify settings.
    authorized = (
        (member_id == project["creator_id"]) or
        (member_role == "project_manager") or
        (member_id in project["members"])
    )

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' "
            "does not have permission to modify project settings."
        )

    # Perform a shallow copy of the settings to avoid accidental mutation
    updated_settings = copy.deepcopy(project["settings"])
    # Merge new settings (new keys overwrite existing ones)
    updated_settings.update(fresh_settings)

    # Update the project in place
    PROJECTS_DB[proj_id]["settings"] = updated_settings

    return f"Project '{proj_id}' settings successfully updated."


# Example usage (uncomment to test):
# try:
#     msg = alter_project_preferences(
#         member_id="user_456",
#         member_role="team_member",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(repr(e))