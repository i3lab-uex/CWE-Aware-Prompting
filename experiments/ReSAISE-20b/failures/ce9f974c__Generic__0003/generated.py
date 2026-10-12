from __future__ import annotations

import copy
from typing import Dict, Any

# Mock database of projects. In a real system this would be replaced by
# persistent storage (e.g., a database or an ORM).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_b", "user_c"],
        # The settings are stored as a dictionary of key/value pairs.
        "settings": {
            "deadline": "2025-12-31",
            "visibility": "private",
        },
    }
}


def change_project_settings(
    owner_id: str,
    access_level: str,
    proj_id: str,
    modifications: Dict[str, Any],
) -> str:
    """
    Update the settings of a project.

    Parameters
    ----------
    owner_id : str
        Identifier of the user attempting to modify the project.
    access_level : str
        Role of the user, e.g. 'project_manager', 'team_member', or 'viewer'.
    proj_id : str
        Identifier of the project to modify.
    modifications : dict
        Key/value pairs representing new configuration values.

    Returns
    -------
    str
        Success message.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in ``PROJECTS_DB``.
    """

    # 1. Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with id '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Determine if the user has sufficient rights.
    #    * The creator of the project always has full rights.
    #    * A user with role 'project_manager' can also modify settings.
    has_permission = False
    if owner_id == project["creator_id"]:
        has_permission = True
    elif access_level == "project_manager" and owner_id in project.get("members", []):
        has_permission = True

    if not has_permission:
        raise PermissionError(
            f"User '{owner_id}' does not have permission to modify project '{proj_id}'."
        )

    # 3. Merge the modifications into the existing settings.
    #    Use a shallow copy to avoid mutating the original dict in case of failure.
    new_settings = copy.deepcopy(project["settings"])
    for key, value in modifications.items():
        # Basic validation: reject attempts to modify immutable keys.
        if key not in new_settings:
            raise ValueError(f"Invalid setting key: '{key}'.")
        new_settings[key] = value

    # 4. Persist the changes back to the database.
    project["settings"] = new_settings

    return (
        f"Project '{proj_id}' settings updated successfully by user "
        f"'{owner_id}'."
    )