import logging
from typing import Dict

# Configure basic logger for debugging and audit purposes
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(module)s] %(message)s",
)

# Sample in-memory projects database
PROJECTS_DB: Dict[str, dict] = {
    "proj1": {
        "project_id": "proj1",
        "creator_id": "userA",
        "members": ["userB", "userC"],
        "settings": {"deadline": "2024-12-31", "visibility": "private"},
    },
    # Add more projects as needed
}


def modify_project_settings(
    user_id: str,
    user_role: str,
    project_id: str,
    new_settings: dict,
) -> str:
    """
    Modify the settings of a project after performing strict authorization checks.

    Parameters
    ----------
    user_id : str
        The ID of the user attempting to modify project settings.
    user_role : str
        Role of the user (e.g., 'project_manager', 'team_member', or 'viewer').
    project_id : str
        The ID of the project being modified.
    new_settings : dict
        New settings to apply.

    Returns
    -------
    str
        Confirmation message if the update succeeded.

    Raises
    ------
    ValueError
        If the project does not exist.
    PermissionError
        If the user is not authorized to modify settings.

    Notes
    -----
    Only users with role 'project_manager' and who are either the creator of the
    project or a member listed in the project's 'members' list may modify settings.
    """
    # Step 1: Ensure the project exists
    project = PROJECTS_DB.get(project_id)
    if not project:
        logging.error("Project %s does not exist", project_id)
        raise ValueError(f"Project {project_id} not found")

    # Step 2: Authorization checks
    if user_role != "project_manager":
        logging.warning(
            "Unauthorized role '%s' attempted to modify project %s",
            user_role,
            project_id,
        )
        raise PermissionError("Only a project manager can modify settings")

    # The user must be the creator or a member of the project
    if user_id != project["creator_id"] and user_id not in project.get("members", []):
        logging.warning(
            "User %s is not authorized to modify project %s",
            user_id,
            project_id,
        )
        raise PermissionError("User is not a member or creator of the project")

    # Step 3: Apply new settings (deep copy to avoid accidental references)
    try:
        updated_settings = {**project["settings"], **new_settings}
    except Exception as exc:  # pragma: no cover
        logging.exception("Failed to merge settings for project %s", project_id)
        raise ValueError(f"Invalid settings format: {exc}") from exc

    # Update the project's settings
    project["settings"] = updated_settings
    logging.info(
        "User %s updated settings for project %s: %s",
        user_id,
        project_id,
        new_settings,
    )

    return f"Project {project_id} settings updated successfully."