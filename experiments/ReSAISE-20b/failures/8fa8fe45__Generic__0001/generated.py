# -*- coding: utf-8 -*-

"""
Project Management Module

Provides a function to alter project preferences while enforcing
role‑based access control and protecting against unauthorized updates.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample in‑memory projects database
# --------------------------------------------------------------------------- #
PROJECTS_DB = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_1001",
        "members": ["user_1001", "user_2002"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Additional projects can be added here
}


# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #
def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: dict,
) -> str:
    """
    Update the settings of a project after verifying that the caller is authorized.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the user in the platform. Accepted values:
            - 'project_manager'
            - 'team_member'
            - 'viewer'
    proj_id : str
        Identifier of the project to update.
    fresh_settings : dict
        New settings key/value pairs to apply.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify project settings.
    KeyError
        If the project ID does not exist in `PROJECTS_DB`.
    ValueError
        If `fresh_settings` is not a dictionary.
    """

    # Validate input types
    if not isinstance(fresh_settings, dict):
        raise ValueError("fresh_settings must be a dictionary")

    # Retrieve project
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' not found") from exc

    # Authorization logic
    is_creator = member_id == project["creator_id"]
    has_manager_privileges = member_role.lower() == "project_manager"

    if not (is_creator or has_manager_privileges):
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' "
            "does not have permission to modify project settings."
        )

    # Merge new settings
    project["settings"].update(fresh_settings)

    return f"Project '{proj_id}' settings updated successfully."


# --------------------------------------------------------------------------- #
# Example usage (for testing purposes only)
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    try:
        msg = alter_project_preferences(
            member_id="user_1001",
            member_role="project_manager",
            proj_id="proj_001",
            fresh_settings={"visibility": "public", "deadline": "2025-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Error: {e}")