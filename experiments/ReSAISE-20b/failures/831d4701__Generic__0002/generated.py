import json

# Sample in‑memory database of projects.
PROJECTS_DB = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed.
}

def update_project_configurations(uid: str, role: str, pid: str, settings: dict) -> str:
    """
    Update the configuration of a project if the caller has sufficient rights.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting the update.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project to modify.
    settings : dict
        New configuration for the project.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to update project settings.
    KeyError
        If the project ID does not exist in the database.
    TypeError
        If `settings` is not a dictionary.
    """
    # Validate that the project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project ID '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Validate settings type
    if not isinstance(settings, dict):
        raise TypeError("Settings must be a dictionary.")

    # Authorization logic:
    # - The project creator can always update.
    # - Users with role 'project_manager' are also allowed.
    if uid != project["creator_id"] and role.lower() != "project_manager":
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project settings."
        )

    # Update the project's settings
    project["settings"] = settings

    return f"Project '{pid}' settings updated successfully by user '{uid}'."

# Example usage (uncomment to test)
# try:
#     msg = update_project_configurations(
#         uid="user123",
#         role="team_member",
#         pid="proj1",
#         settings={"deadline": "2025-01-15", "visibility": "public"}
#     )
#     print(msg)
# except Exception as e:
#     print(e)