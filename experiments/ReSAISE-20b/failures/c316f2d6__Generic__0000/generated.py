import logging

# Example data structures (replace with real ones in production)
PROJECTS = {
    # project_id: {'owner_id': int, 'members': set of user_ids}
}

USERS = {
    # user_id: {'role': str, ...}
}

# Configure a basic logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Allow project owners to add or remove members from their project,
    while admins can modify any project.

    Parameters
    ----------
    current_user_id : int
        ID of the user invoking the action.
    project_id : int
        ID of the project to modify.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        ID of the user to add or remove.

    Returns
    -------
    bool
        True if the action succeeded, False otherwise.
    """
    # Validate inputs
    if action not in {"add", "remove"}:
        logger.warning("Invalid action: %s", action)
        return False

    project = PROJECTS.get(project_id)
    if not project:
        logger.warning("Project %s does not exist", project_id)
        return False

    # Check that the target user exists
    if target_user_id not in USERS:
        logger.warning("Target user %s does not exist", target_user_id)
        return False

    # Get the role of the current user
    current_role = USERS.get(current_user_id, {}).get("role", "")
    if not current_role:
        logger.warning("Current user %s has no role defined", current_user_id)
        return False

    # Permission check: admins can always modify; owners only for their own projects
    if current_role != "admin":
        if project.get("owner_id") != current_user_id:
            logger.warning(
                "User %s is not the owner of project %s",
                current_user_id,
                project_id,
            )
            return False

    members = project.setdefault("members", set())

    if action == "add":
        if target_user_id in members:
            logger.info(
                "User %s is already a member of project %s",
                target_user_id,
                project_id,
            )
            return False
        members.add(target_user_id)
    else:  # action == "remove"
        if target_user_id not in members:
            logger.info(
                "User %s is not a member of project %s",
                target_user_id,
                project_id,
            )
            return False
        members.remove(target_user_id)

    logger.info(
        "User %s performed '%s' on user %s for project %s",
        current_user_id,
        action,
        target_user_id,
        project_id,
    )
    return True