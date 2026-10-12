# -*- coding: utf-8 -*-
"""
Project settings modification module.

The core function `modify_project_settings` updates the settings of a project
only if the user is authorized.  Authorization rules:

* The user must be either:
    * a project manager (`user_role == 'project_manager'`), or
    * the creator of the project.
* Users with roles `team_member` or `viewer` are not allowed to modify settings.

If the project does not exist a ``ValueError`` is raised.  The function
returns a confirmation string on success or an error message otherwise.
"""

from __future__ import annotations

# Example in‑memory database.  In a real application this would be
# replaced by a persistent store (SQL, NoSQL, etc.).
PROJECTS_DB: dict[str, dict] = {
    # Example project for demonstration purposes
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_456", "user_789"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict,
) -> str:
    """
    Update the settings of a project if the user is authorized.

    Parameters
    ----------
    user_id : str
        ID of the user attempting to modify settings.
    user_role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        ID of the target project.
    new_settings : dict
        Dictionary containing the settings to apply.

    Returns
    -------
    str
        Confirmation message on success or an authorization error message.

    Raises
    ------
    ValueError
        If the project with ``project_id`` does not exist.
    """
    # Validate existence of the project
    if project_id not in PROJECTS_DB:
        raise ValueError(f"Project '{project_id}' does not exist.")

    project = PROJECTS_DB[project_id]

    # Authorization check
    is_creator = user_id == project["creator_id"]
    has_manager_role = user_role.lower() == "project_manager"

    if not (is_creator or has_manager_role):
        return (
            f"Authorization error: user '{user_id}' "
            f"(role: {user_role}) cannot modify settings for project '{project_id}'."
        )

    # Merge new settings with existing ones.  This simple approach keeps
    # unspecified keys unchanged.
    project["settings"].update(new_settings)

    return (
        f"Settings for project '{project_id}' successfully updated "
        f"by user '{user_id}'."
    )