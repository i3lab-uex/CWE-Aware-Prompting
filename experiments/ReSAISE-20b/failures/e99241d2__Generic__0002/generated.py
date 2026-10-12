#!/usr/bin/env python3
"""
Project configuration updater for a shared project management system.
"""

from typing import Dict, Any

# Mock database of projects
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Example entry:
    # "proj_001": {
    #     "project_id": "proj_001",
    #     "creator_id": "emp_123",
    #     "members": ["emp_456", "emp_789"],
    #     "settings": {"deadline": "2024-12-31", "visibility": "private"}
    # }
}

def update_project_configurations(
    emp_id: str,
    role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    emp_id : str
        Unique identifier of the user attempting the update.
    role : str
        Role of the user ('project_manager', 'team_member', or 'viewer').
    proj_id : str
        Identifier of the project to be updated.
    updated_settings : dict
        Dictionary containing the new settings for the project.

    Returns
    -------
    str
        Success message indicating that the update was applied.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID is not found in the database.
    ValueError
        If `updated_settings` is not a dictionary or is empty.
    """
    # Validate input
    if not isinstance(updated_settings, dict) or not updated_settings:
        raise ValueError("`updated_settings` must be a non‑empty dictionary")

    # Retrieve the project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project ID '{proj_id}' does not exist") from exc

    # Authorization logic
    is_creator = emp_id == project.get("creator_id")
    is_member = emp_id in project.get("members", [])
    allowed_roles = {"project_manager"}  # roles that can modify settings

    if not (is_creator or is_member) and role not in allowed_roles:
        raise PermissionError(
            f"User '{emp_id}' with role '{role}' is not authorized "
            f"to update project '{proj_id}'."
        )

    # Apply updates
    project_settings = project.setdefault("settings", {})
    project_settings.update(updated_settings)

    return f"Project '{proj_id}' settings successfully updated by user '{emp_id}'."

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     PROJECTS_DB["proj_001"] = {
#         "project_id": "proj_001",
#         "creator_id": "emp_123",
#         "members": ["emp_456", "emp_789"],
#         "settings": {"deadline": "2024-12-31", "visibility": "private"}
#     }
#     print(update_project_configurations("emp_123", "project_manager", "proj_001",
#                                          {"visibility": "public"}))