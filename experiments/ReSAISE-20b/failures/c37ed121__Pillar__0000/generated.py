# adjust_project_options.py

"""
Utility to modify project settings with proper authorization checks.

Author: OpenAI
"""

from typing import Dict, Any

# Sample in‑memory projects database.
# In a real application this would be replaced by persistent storage (e.g., a DB).
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2024-12-31"},
    },
    # ... other projects
}

# Define roles that are allowed to modify project settings.
ALLOWED_ROLES = {"project_manager", "admin"}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the editor is authorized.

    Parameters
    ----------
    editor_id : str
        The ID of the user attempting to modify the project.
    editor_role : str
        The role of the editor (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        The ID of the project to update.
    updated_settings : dict
        A dictionary containing settings keys and their new values.

    Returns
    -------
    str
        Confirmation message upon successful update.

    Raises
    ------
    PermissionError
        If the editor is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # 1. Validate that the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # 2. Check authorization
    is_creator = editor_id == project["creator_id"]
    has_role_permission = editor_role in ALLOWED_ROLES
    is_member = editor_id in project.get("members", [])

    # Only creators, admins or project managers can edit settings.
    if not (is_creator or has_role_permission):
        # Even a member cannot modify unless role allows
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' is not authorized "
            "to modify project settings."
        )

    # 3. Perform the update
    for key, value in updated_settings.items():
        project["settings"][key] = value

    return f"Project '{proj_id}' settings successfully updated by user '{editor_id}'."