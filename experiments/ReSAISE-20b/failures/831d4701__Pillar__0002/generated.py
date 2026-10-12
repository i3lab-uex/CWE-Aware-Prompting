# update_project_configurations.py

from copy import deepcopy
from typing import Dict, Any


# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": {"user_456", "user_789"},
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # ... other projects
}


def _is_authorized(uid: str, role: str, project: Dict[str, Any]) -> bool:
    """
    Determine if a user is authorized to modify project settings.

    A user may modify settings only if:
      * They are the creator of the project, OR
      * They are a member of the project and have the role 'project_manager'.
    """
    if uid == project["creator_id"]:
        return True
    if role == "project_manager" and uid in project.get("members", set()):
        return True
    return False


def update_project_configurations(
    uid: str, role: str, pid: str, settings: Dict[str, Any]
) -> str:
    """
    Update the configuration of a project.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting the update.
    role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    pid : str
        Identifier of the project to modify.
    settings : dict
        New configuration values for the project.

    Returns
    -------
    str
        Success message indicating that settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have sufficient rights.
    KeyError
        If the project ID is unknown.
    ValueError
        If the settings dictionary contains disallowed keys.

    Notes
    -----
    * Only a limited set of configuration keys are allowed to be updated.
      This prevents arbitrary injection of malicious data.
    * The function performs a shallow copy of the provided settings to avoid
      accidental mutation of caller objects.
    """
    # 1. Validate project existence
    if pid not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{pid}' does not exist.")

    project = PROJECTS_DB[pid]

    # 2. Authorization check
    if not _is_authorized(uid, role, project):
        raise PermissionError("User is not authorized to update project settings.")

    # 3. Whitelist of allowed configuration keys
    ALLOWED_KEYS = {"visibility", "deadline", "notification_emails"}

    # 4. Validate settings keys
    invalid_keys = set(settings) - ALLOWED_KEYS
    if invalid_keys:
        raise ValueError(f"Attempt to modify disallowed keys: {invalid_keys}")

    # 5. Update settings safely
    new_settings = deepcopy(project["settings"])
    new_settings.update(settings)
    project["settings"] = new_settings

    return f"Project '{pid}' settings updated successfully."


# Example usage (for local testing only)
if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            uid="user_456",
            role="project_manager",
            pid="proj_001",
            settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")