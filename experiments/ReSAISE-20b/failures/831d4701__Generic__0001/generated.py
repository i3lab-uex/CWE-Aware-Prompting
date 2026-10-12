from typing import Dict, Any

# Example in‑memory projects database. In a real system this would be replaced
# by persistent storage (e.g., a relational database or NoSQL store).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_1": {
        "project_id": "proj_1",
        "creator_id": "user_a",
        "members": {"user_a", "user_b"},
        "settings": {
            "visibility": "private",
            "deadline": "2025-12-31"
        }
    },
    # ... more projects
}


def update_project_configurations(uid: str, role: str, pid: str,
                                  settings: Dict[str, Any]) -> str:
    """
    Update the configuration of a project if the user has sufficient rights.

    Parameters
    ----------
    uid : str
        The identifier of the user attempting to update settings.
    role : str
        The user's role, e.g., 'project_manager', 'team_member', or 'viewer'.
    pid : str
        The identifier of the project to be modified.
    settings : dict
        A dictionary containing new configuration values.

    Returns
    -------
    str
        Success message indicating that the settings have been updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights to modify the project.
    KeyError
        If the project ID is not found in the database.
    """

    # Validate project existence
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project ID '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # Authorization logic
    authorized = False

    # 1. Project creator is always allowed to modify settings.
    if uid == project["creator_id"]:
        authorized = True

    # 2. Project managers have full rights.
    if role == "project_manager":
        authorized = True

    # 3. Team members may modify settings if they are explicitly listed.
    if role == "team_member" and uid in project["members"]:
        authorized = True

    # 4. Viewers are never allowed to modify settings.
    if role == "viewer":
        authorized = False

    # 5. Any other roles are treated as unauthorized.
    if not authorized:
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{pid}'."
        )

    # Perform the update safely: merge existing settings with new ones.
    project["settings"].update(settings)

    return f"Project '{pid}' settings successfully updated by user '{uid}'."