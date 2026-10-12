# -*- coding: utf-8 -*-
"""
Module containing the `update_project_configurations` function.
"""

from typing import Dict

# Sample in-memory database of projects
PROJECTS_DB: Dict[str, dict] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "user123",
        "members": ["user123", "user456"],
        "settings": {
            "deadline": "2024-12-31",
            "visibility": "private",
        },
    },
    # Additional projects can be added here
}


def update_project_configurations(
    u_id: str,
    u_role: str,
    proj_id: str,
    modified_settings: Dict[str, any],
) -> str:
    """
    Update the configuration settings of a project.

    Parameters
    ----------
    u_id : str
        ID of the user attempting to modify the project.
    u_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        Identifier of the project to be updated.
    modified_settings : dict
        Dictionary containing the settings to update.

    Returns
    -------
    str
        Success message if the update was performed.

    Raises
    ------
    PermissionError
        If the user is not authorized to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """
    # --- Authorization check ---------------------------------------------
    # Retrieve the project; if it does not exist raise KeyError
    try:
        project = PROJECTS_DB[proj_id]
    except KeyError as exc:
        raise KeyError(f"Project '{proj_id}' not found.") from exc

    # Only the creator or a user with role 'project_manager' can modify settings.
    authorized = (
        u_id == project["creator_id"] or
        (u_role.lower() == "project_manager" and u_id in project["members"])
    )

    if not authorized:
        raise PermissionError(
            f"User '{u_id}' with role '{u_role}' is not authorized to modify project '{proj_id}'."
        )

    # --- Update settings ---------------------------------------------
    # Merge the modified settings into existing ones.
    project_settings = project.setdefault("settings", {})
    for key, value in modified_settings.items():
        # Basic validation: ensure the key exists in current settings
        if key not in project_settings:
            raise ValueError(f"Setting '{key}' is not a valid configuration key.")
        project_settings[key] = value

    return f"Project '{proj_id}' settings updated successfully."


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     try:
#         result = update_project_configurations(
#             u_id="user123",
#             u_role="project_manager",
#             proj_id="proj1",
#             modified_settings={"deadline": "2025-01-15"}
#         )
#         print(result)
#     except Exception as e:
#         print(f"Error: {e}")