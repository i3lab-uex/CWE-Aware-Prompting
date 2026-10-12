import logging
from typing import Dict, List

# Example data structures – in real use these would be populated elsewhere
PROJECTS: Dict[int, Dict] = {}
USERS: Dict[int, str] = {}

# Configure a basic logger for debugging purposes
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int
) -> bool:
    """
    Modify the membership list of a project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        Target project ID.
    act_type : str
        'add' or 'remove'.
    tgt_user_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action type early
    if act_type not in {"add", "remove"}:
        raise ValueError(f"Invalid action type: {act_type!r}")

    # Retrieve the project and executing user role
    project = PROJECTS.get(prjct_id)
    if not project:
        logger.warning("Project %s does not exist.", prjct_id)
        return False

    exec_role = USERS.get(executing_user_id, "user")

    # Permission check
    if exec_role != "admin" and executing_user_id != project.get("owner_id"):
        logger.warning(
            "User %s (%s) is not authorized to modify project %s.",
            executing_user_id,
            exec_role,
            prjct_id
        )
        return False

    # Ensure target user exists
    if tgt_user_id not in USERS:
        logger.warning("Target user %s does not exist.", tgt_user_id)
        return False

    members: List[int] = project.setdefault("members", [])

    if act_type == "add":
        if tgt_user_id in members:
            logger.info(
                "User %s is already a member of project %s.",
                tgt_user_id,
                prjct_id
            )
            return False
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            logger.info(
                "User %s is not a member of project %s.",
                tgt_user_id,
                prjct_id
            )
            return False
        if tgt_user_id == project.get("owner_id"):
            logger.warning(
                "Attempted to remove the owner (%s) from project %s.",
                tgt_user_id,
                prjct_id
            )
            return False
        members.remove(tgt_user_id)

    logger.info(
        "User %s performed '%s' on user %s for project %s.",
        executing_user_id,
        act_type,
        tgt_user_id,
        prjct_id
    )
    return True