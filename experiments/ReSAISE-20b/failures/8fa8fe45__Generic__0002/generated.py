import copy

# Sample in‑memory database of projects. In a real system this would be replaced by
# persistent storage (e.g., a database or an external service).
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {
            "visibility": "private",
            "notifications_enabled": True,
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
    Update project settings if the caller has sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to modify.
    fresh_settings : dict
        Dictionary containing new settings. Keys that are not present in the
        existing project will be ignored to avoid accidental schema changes.

    Returns
    -------
    str
        Success message when settings are updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify project settings.
    KeyError
        If the specified project does not exist in `PROJECTS_DB`.
    """
    # Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with id '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    is_creator = member_id == project["creator_id"]
    has_membership = member_id in project.get("members", [])

    # Only a creator or a user with the 'project_manager' role can update settings.
    if not (is_creator or member_role == "project_manager"):
        raise PermissionError(
            f"User '{member_id}' does not have permission to modify settings for project '{proj_id}'."
        )

    # Sanity check: ensure the member is at least part of the project (except for creator)
    if not has_membership and not is_creator:
        raise PermissionError(
            f"User '{member_id}' is not a member of project '{proj_id}'."
        )

    # Update only existing keys to avoid accidental schema drift.
    current_settings = project.get("settings", {})
    for key, value in fresh_settings.items():
        if key in current_settings:
            current_settings[key] = copy.deepcopy(value)

    # Persist the changes back to the in‑memory DB.
    project["settings"] = current_settings

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (this block is for illustration and would normally be in a separate test file):
if __name__ == "__main__":
    try:
        msg = alter_project_preferences(
            member_id="user_123",
            member_role="project_manager",
            proj_id="proj_001",
            fresh_settings={"visibility": "public", "notifications_enabled": False},
        )
        print(msg)
    except Exception as exc:
        print(f"Error: {exc}")