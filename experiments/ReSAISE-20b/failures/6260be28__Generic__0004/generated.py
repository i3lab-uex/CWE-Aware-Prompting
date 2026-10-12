import copy

# Example in‑memory database of projects.
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict,
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        The role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        The ID of the project being modified.
    new_settings : dict
        The new settings to apply to the project.

    Returns
    -------
    str
        Confirmation message if update succeeded, otherwise an authorization error string.

    Raises
    ------
    ValueError
        If the project does not exist.
    """
    # 1. Verify that the project exists
    if project_id not in PROJECTS_DB:
        raise ValueError(f"Project '{project_id}' does not exist.")

    project = PROJECTS_DB[project_id]

    # 2. Authorization check
    authorized_roles = {"project_manager"}  # roles that can modify settings
    is_creator = user_id == project["creator_id"]

    if not (user_role in authorized_roles or is_creator):
        return (
            f"Authorization error: user '{user_id}' with role "
            f"'{user_role}' is not allowed to modify settings for project '{project_id}'."
        )

    # 3. Perform the update
    # We make a shallow copy to avoid mutating input directly.
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(new_settings)

    # 4. Persist the changes back to the DB
    project["settings"] = updated_settings

    return (
        f"Project '{project_id}' settings successfully updated by user "
        f"'{user_id}'. New settings: {updated_settings}"
    )