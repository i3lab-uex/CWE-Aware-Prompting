import copy

# Mock database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_a", "user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Additional projects can be added here.
}


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: dict,
) -> str:
    """
    Update project settings for a given project.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the user ('project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    fresh_settings : dict
        New settings values to merge into the existing project settings.

    Returns
    -------
    str
        Success message if update is authorized and performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project settings.
    KeyError
        If the specified project ID is not found in `PROJECTS_DB`.
    """
    # Verify that the project exists.
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    # 1. The creator can always modify settings.
    # 2. A project_manager who is also a member of the project can modify.
    # 3. Other roles (team_member, viewer) are not allowed to modify settings.
    authorized = False
    if member_id == project["creator_id"]:
        authorized = True
    elif (
        member_role.lower() == "project_manager"
        and member_id in project["members"]
    ):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized to modify settings for project '{proj_id}'."
        )

    # Merge fresh_settings into existing settings.
    # A shallow copy is sufficient as settings are expected to be simple types.
    project["settings"].update(copy.deepcopy(fresh_settings))

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test):
# try:
#     msg = alter_project_preferences(
#         member_id="user_a",
#         member_role="project_manager",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public", "deadline": "2025-01-15"},
#     )
#     print(msg)
# except Exception as e:
#     print(e)