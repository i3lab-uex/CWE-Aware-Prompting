from __future__ import annotations

import logging
from typing import Dict, Any

# Example data structures (should be replaced with real persistence in production)
PROJECTS: Dict[int, Dict[str, Any]] = {
    # project_id: {"owner_id": int, "members": set[int]}
}

USERS: Dict[int, str] = {
    # user_id: "role"  (roles: "admin", "owner", "member")
}

# Configure a logger for audit purposes
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return USERS.get(user_id) == "admin"


def _is_owner(project: Dict[str, Any], user_id: int) -> bool:
    """Return True if the user is the owner of the project."""
    return project.get("owner_id") == user_id


def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    current_user_id : int
        The user performing the action.
    project_id : int
        Identifier of the target project.
    action : str
        Either 'add' or 'remove'.
    target_user_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    ValueError
        If an unsupported action is provided.
    KeyError
        If the project or target user does not exist.

    Notes
    -----
    * Only admins can modify any project.
    * Project owners can only modify their own projects.
    * All operations are logged for auditability.
    """
    if action not in {"add", "remove"}:
        raise ValueError("action must be 'add' or 'remove'")

    # Retrieve project and ensure it exists
    try:
        project = PROJECTS[project_id]
    except KeyError as exc:
        logger.warning("Project %s not found", project_id)
        raise KeyError(f"Project {project_id} does not exist") from exc

    # Retrieve target user to ensure they exist
    if target_user_id not in USERS:
        logger.warning("Target user %s does not exist", target_user_id)
        raise KeyError(f"User {target_user_id} does not exist")

    # Authorization check: admin or owner of the project
    if not (_is_admin(current_user_id) or _is_owner(project, current_user_id)):
        logger.warning(
            "User %s attempted unauthorized %s on project %s",
            current_user_id,
            action,
            project_id,
        )
        return False

    members: set[int] = project.setdefault("members", set())

    if action == "add":
        if target_user_id in members:
            logger.info(
                "User %s already a member of project %s", target_user_id, project_id
            )
            return False  # Already a member; no change made
        members.add(target_user_id)
        logger.info(
            "User %s added to project %s by user %s",
            target_user_id,
            project_id,
            current_user_id,
        )
    else:  # action == "remove"
        if target_user_id not in members:
            logger.info(
                "User %s is not a member of project %s", target_user_id, project_id
            )
            return False  # Not a member; nothing to remove
        members.remove(target_user_id)
        logger.info(
            "User %s removed from project %s by user %s",
            target_user_id,
            project_id,
            current_user_id,
        )

    return True