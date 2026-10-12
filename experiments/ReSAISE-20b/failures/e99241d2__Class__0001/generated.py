import datetime
from typing import Dict, Any

# Simulated in-memory project database
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "emp_1001",
        "members": ["emp_1002", "emp_1003"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Additional projects can be added here
}


class PermissionError(Exception):
    """Raised when a user does not have permission to modify project settings."""


def update_project_configurations(
    emp_id: str,
    role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Update project settings if the user is authorized.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the employee attempting the modification.
    role : str
        Role of the employee. Expected values: 'project_manager', 'team_member', or 'viewer'.
    proj_id : str
        Identifier of the project to update.
    updated_settings : dict
        Dictionary containing the new settings for the project.

    Returns
    -------
    str
        Success message indicating that the project was updated.

    Raises
    ------
    PermissionError
        If the user is not authorized to update the project settings.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # Verify that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project with ID '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic
    is_creator = emp_id == project["creator_id"]
    is_member = emp_id in project.get("members", [])
    allowed_roles = {"project_manager"}  # Only project managers can modify settings

    # CWE-863 protection: ensure that all checks are performed together
    authorized = (
        role in allowed_roles and (is_creator or is_member)
    )

    if not authorized:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized to modify project settings."
        )

    # Perform the update
    project["settings"].update(updated_settings)
    project["last_modified_by"] = emp_id
    project["last_modified_at"] = datetime.datetime.utcnow().isoformat()

    return f"Project '{proj_id}' settings updated successfully."