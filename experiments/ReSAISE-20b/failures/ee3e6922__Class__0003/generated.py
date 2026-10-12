import copy
from typing import Dict, Any

# Mock database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # Add more projects as needed
}


def change_project_config(
    uid: str, role: str, proj: str, settings_update: Dict[str, Any]
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    uid : str
        Unique identifier of the user attempting to modify the project.
    role : str
        Role description of the caller (e.g., 'project_manager', 'team_member', 'viewer').
    proj : str
        Identifier of the project to update.
    settings_update : dict
        Dictionary containing updated settings values.

    Returns
    -------
    str
        Success message confirming the update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in the database.
    """
    # Validate that the project exists
    if proj not in PROJECTS_DB:
        raise KeyError(f"Project '{proj}' does not exist.")

    project = PROJECTS_DB[proj]

    # Authorization: only the creator or a user with role 'project_manager'
    # can modify project settings. Additionally, the uid must be a member.
    authorized = (
        (uid == project["creator_id"] and role in {"project_manager", "creator"})
        or (role == "project_manager")
    ) and uid in project["members"]

    if not authorized:
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized to modify project '{proj}'."
        )

    # Merge settings_update into existing settings
    updated_settings = copy.deepcopy(project["settings"])
    for key, value in settings_update.items():
        # Basic validation: disallow setting removal by providing None
        if value is None:
            raise ValueError(f"Setting '{key}' cannot be set to None.")
        updated_settings[key] = value

    # Persist the updated settings
    project["settings"] = updated_settings

    return f"Project '{proj}' settings successfully updated by user '{uid}'."