# update_project_configurations.py

from typing import Dict

# Example in‑memory database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_admin",
        "members": ["user_admin", "user_pm1"],
        "settings": {"deadline": "2025-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(uid: str, role: str, pid: str, settings: Dict) -> str:
    """
    Update the configuration of a project if the caller has sufficient rights.

    Parameters
    ----------
    uid : str
        The identifier of the user attempting to update settings.
    role : str
        The role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        The identifier of the project being modified.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the project ID is not found in `PROJECTS_DB`.
    """
    # Validate that the project exists
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Only the creator or a user with role 'project_manager' can update settings
    authorized = False

    # Check if the user is the creator
    if uid == project["creator_id"]:
        authorized = True

    # Check role-based permission
    if role == "project_manager":
        # Allow project managers regardless of creator status
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to update project '{pid}'."
        )

    # Perform the update safely
    if not isinstance(settings, dict):
        raise ValueError("settings must be a dictionary.")

    # Merge new settings into existing ones
    project["settings"].update(settings)

    return f"Project '{pid}' settings updated successfully by user '{uid}'."