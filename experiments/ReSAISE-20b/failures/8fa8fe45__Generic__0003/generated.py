import copy
from typing import Dict, Any

# Example in‑memory database of projects.
PROJECTS_DB: Dict[str, Dict[str, Any]] = {
    # Sample project structure
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_a",
        "members": ["user_a", "user_b", "user_c"],
        "settings": {
            "visibility": "private",
            "deadline": "2024-12-31",
        },
    },
    # Add more projects as needed
}


def alter_project_preferences(
    member_id: str,
    member_role: str,
    proj_id: str,
    fresh_settings: Dict[str, Any],
) -> str:
    """
    Update the settings of a project if the user has sufficient permissions.

    Parameters
    ----------
    member_id : str
        ID of the user attempting to modify the project.
    member_role : str
        Role of the user (e.g., 'project_manager', 'team_member', 'viewer').
    proj_id : str
        ID of the project to be updated.
    fresh_settings : dict
        Dictionary containing new settings for the project.

    Returns
    -------
    str
        Success message indicating that the settings were updated.

    Raises
    ------
    PermissionError
        If the user does not have permission to modify the project.
    KeyError
        If the specified project ID does not exist in PROJECTS_DB.
    """
    # Ensure project exists
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project {proj_id} does not exist.")

    project = PROJECTS_DB[proj_id]

    # Authorization logic:
    #   * The creator can always modify.
    #   * A user with role 'project_manager' who is a member can modify.
    #   * Other roles are denied.
    authorized = False
    if member_id == project["creator_id"]:
        authorized = True
    elif (
        member_role.lower() == "project_manager"
        and member_id in project["members"]
    ):
        authorized = True

    if not authorized:
        raise PermissionError(
            f"User {member_id} with role '{member_role}' "
            "is not authorized to modify project settings."
        )

    # Update settings safely
    if not isinstance(fresh_settings, dict):
        raise ValueError("fresh_settings must be a dictionary.")

    # Create a shallow copy to avoid unintended side effects
    updated_settings = copy.deepcopy(project["settings"])
    updated_settings.update(fresh_settings)
    project["settings"] = updated_settings

    return f"Project {proj_id} settings updated successfully."