# ──────────────────────────────────────────────────────────────── #
#  project_management.py                                          #
#  Implements `update_project_configurations` for a mock platform. #
# ──────────────────────────────────────────────────────────────── #

from typing import Dict, Any

# Mock database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj-001": {
        "project_id": "proj-001",
        "creator_id": "user-100",
        "members": {"user-101", "user-102"},
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def update_project_configurations(
    uid: str, role: str, pid: str, settings: Dict[str, Any]
) -> str:
    """
    Update project configuration if the user has sufficient rights.

    Parameters
    ----------
    uid : str
        Identifier of the user attempting to update settings.
    role : str
        Role of the user. Accepted values: 'project_manager', 'team_member',
        'viewer'.
    pid : str
        Identifier of the project to modify.
    settings : dict
        New configuration dictionary for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    ValueError
        If `settings` is not a dictionary.

    Notes
    -----
    * Only the project creator or users with role 'project_manager'
      who are also members of the project can modify settings.
    * The update merges new settings into existing ones; keys not present
      in `settings` remain unchanged.
    * Sensitive fields (e.g., 'creator_id') cannot be overridden via
      `settings` to prevent privilege escalation.
    """

    # Validate inputs
    if not isinstance(settings, dict):
        raise ValueError("`settings` must be a dictionary.")

    # Retrieve the project
    try:
        project = PROJECTS_DB[pid]
    except KeyError as exc:
        raise KeyError(f"Project ID '{pid}' does not exist.") from exc

    # Check authorization
    is_creator = uid == project["creator_id"]
    is_manager_role = role.lower() == "project_manager"
    is_member = uid in project["members"]

    if not (is_creator or (is_manager_role and is_member)):
        raise PermissionError(
            f"User '{uid}' with role '{role}' is not authorized "
            "to update project settings."
        )

    # Prevent overriding immutable fields
    immutable_keys = {"project_id", "creator_id", "members"}
    for key in immutable_keys:
        if key in settings:
            raise ValueError(f"Cannot modify immutable field '{key}' via settings.")

    # Merge new settings into existing ones
    project["settings"].update(settings)

    return f"Project '{pid}' settings successfully updated."


# ──────────────────────────────────────────────────────────────── #
#  Example usage (uncomment to test)                              #
# ──────────────────────────────────────────────────────────────── #

if __name__ == "__main__":
    try:
        msg = update_project_configurations(
            uid="user-101",
            role="project_manager",
            pid="proj-001",
            settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")