# change_project_config.py

from typing import Dict, Any

# Example in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # project_id : {project_id, creator_id, members, settings}
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def change_project_config(uid: str, role: str, proj: str, settings_update: Dict[str, Any]) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting to modify the project.
    role : str
        Role claimed by the user. Expected values are 'project_manager',
        'team_member', or 'viewer'.
    proj : str
        Identifier of the project to be updated.
    settings_update : dict
        Dictionary containing settings to update.

    Returns
    -------
    str
        Success message if the operation is authorized and completed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    ValueError
        If settings_update is not a dictionary.
    """
    # Validate that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Validate that settings_update is a dictionary
    if not isinstance(settings_update, dict):
        raise ValueError("settings_update must be a dictionary.")

    # Authorization logic (CWE‑863 safe implementation)
    # The user must be the creator or a member with an appropriate role.
    is_creator = uid == project["creator_id"]
    is_member = uid in project.get("members", [])

    # Define allowed roles for modification
    ALLOWED_ROLES = {"project_manager"}

    # The role must be one of the allowed roles and the user
    # must actually belong to the project (creator or member).
    if not (
        is_creator
        or (is_member and role in ALLOWED_ROLES)
    ):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Merge the new settings into the existing ones.
    # Only keys present in settings_update are overwritten; others remain unchanged.
    project["settings"].update(settings_update)

    return f"Project '{proj}' settings updated successfully."


# Example usage (uncomment to test)
if __name__ == "__main__":
    try:
        msg = change_project_config(
            uid="user_456",
            role="project_manager",
            proj="proj_001",
            settings_update={"visibility": "public"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")