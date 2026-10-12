import copy
from typing import Dict

# Sample in‑memory database of projects.
PROJECTS_DB: Dict[str, dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_a", "user_b"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: Dict,
) -> str:
    """
    Update project settings for a given project.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify settings.
    member_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to update.
    fresh_settings : dict
        Dictionary containing updated settings.

    Returns
    -------
    str
        Success message if update is authorized and performed.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project does not exist in PROJECTS_DB.
    """

    # Ensure the project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization checks:
    # 1. Only the creator or a project manager can modify settings.
    # 2. The user must be a member of the project.
    is_creator = member_id == project["creator_id"]
    has_role_privilege = member_role.lower() in {"project_manager", "admin"}
    is_member = member_id in project["members"]

    if not (is_creator or has_role_privilege) or not is_member:
        raise PermissionError(
            f"User '{member_id}' with role '{member_role}' is not authorized "
            "to modify settings for project '{proj_id}'."
        )

    # Safely update the settings dictionary
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(fresh_settings)

    # Persist the changes back to the database
    project["settings"] = updated_settings

    return f"Settings for project '{proj_id}' have been successfully updated."


# Example usage (uncomment to test):
# try:
#     msg = alter_project_preferences(
#         member_id="user_a",
#         member_role="project_manager",
#         proj_id="proj_001",
#         fresh_settings={"visibility": "public", "deadline": "2025-01-15"},
#     )
#     print(msg)
# except Exception as e:
#     print(f"Error: {e}")