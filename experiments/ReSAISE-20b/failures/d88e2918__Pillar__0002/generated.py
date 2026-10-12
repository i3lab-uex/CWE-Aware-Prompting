# -*- coding: utf-8 -*-

"""
Project management utilities.
"""

from typing import Dict

# Sample in‑memory database of projects
PROJECTS_DB: Dict[str, Dict] = {
    # Example project structure:
    # "proj_123": {
    #     "project_id": "proj_123",
    #     "creator_id": "user_a",
    #     "members": {"user_a", "user_b"},
    #     "settings": {"name": "Demo Project", "visibility": "private"}
    # }
}

def edit_project_settings(
    member_id: str,
    role: str,
    project_key: str,
    updated_configuration: Dict
) -> str:
    """
    Update the settings of a project if the caller is authorized.

    Parameters
    ----------
    member_id : str
        The unique identifier of the user attempting the modification.
    role : str
        The role of the user ('project_manager', 'team_member', or 'viewer').
    project_key : str
        The identifier of the project whose settings should be changed.
    updated_configuration : dict
        The new configuration values for the project.

    Returns
    -------
    str
        Success message upon successful update.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify project settings.
    KeyError
        If the specified project does not exist.
    """
    # Validate project existence
    if project_key not in PROJECTS_DB:
        raise KeyError(f"Project '{project_key}' does not exist.")

    project = PROJECTS_DB[project_key]

    # Authorization logic:
    # - Only the creator or a user with role 'project_manager' can modify settings.
    # - Additionally, the user must be a member of the project.
    is_creator = (member_id == project["creator_id"])
    has_manager_role = (role.lower() == "project_manager")
    is_member = member_id in project.get("members", set())

    if not (is_creator or has_manager_role) or not is_member:
        raise PermissionError(
            f"User '{member_id}' does not have permission to edit settings "
            f"for project '{project_key}'."
        )

    # Perform the update safely: merge new settings into existing ones
    project_settings = project.get("settings", {})
    if not isinstance(project_settings, dict):
        # Defensive: reset to empty dict if corrupted
        project_settings = {}
    project_settings.update(updated_configuration)
    project["settings"] = project_settings

    return (
        f"Project '{project_key}' settings successfully updated by user "
        f"'{member_id}'."
    )