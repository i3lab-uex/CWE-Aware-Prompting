import logging
from typing import Dict, List

# Example data structures (these would normally be populated elsewhere in the application)
PROJECTS: Dict[int, Dict[str, List[int]]] = {
    # project_id: {'owner_id': int, 'members': [int]}
}
USERS: Dict[int, str] = {
    # user_id: 'admin' or 'user'
}

# Configure logging for audit trail
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [operator:%(operator)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def adjust_team_membership(
    operator_id: int,
    team_project_id: int,
    operation_type: str,
    member_id: int,
) -> bool:
    """
    Add or remove a user from a project team.

    Parameters
    ----------
    operator_id : int
        ID of the user performing the operation.
    team_project_id : int
        Target project ID.
    operation_type : str
        Either 'add' or 'remove'.
    member_id : int
        ID of the user to be added/removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate operator exists
    operator_role = USERS.get(operator_id)
    if not operator_role:
        logging.warning(
            "Operator %s does not exist.", operator_id, extra={"operator": operator_id}
        )
        return False

    # Validate project exists
    project = PROJECTS.get(team_project_id)
    if not project:
        logging.warning(
            "Project %s does not exist.", team_project_id, extra={"operator": operator_id}
        )
        return False

    # Authorization check: operator must be project owner or admin
    if operator_role != "admin" and operator_id != project["owner_id"]:
        logging.warning(
            "Operator %s is not authorized to modify project %s.",
            operator_id,
            team_project_id,
            extra={"operator": operator_id},
        )
        return False

    # Validate member exists
    if member_id not in USERS:
        logging.warning(
            "Member %s does not exist.", member_id, extra={"operator": operator_id}
        )
        return False

    # Perform operation
    members: List[int] = project["members"]
    if operation_type == "add":
        if member_id in members:
            logging.info(
                "Member %s already part of project %s.", member_id, team_project_id,
                extra={"operator": operator_id},
            )
            return False
        members.append(member_id)
    elif operation_type == "remove":
        if member_id not in members:
            logging.info(
                "Member %s not part of project %s.", member_id, team_project_id,
                extra={"operator": operator_id},
            )
            return False
        members.remove(member_id)
    else:
        logging.error(
            "Invalid operation_type '%s'.", operation_type, extra={"operator": operator_id}
        )
        return False

    # Log success
    logging.info(
        "Operator %s performed '%s' on member %s for project %s.",
        operator_id,
        operation_type,
        member_id,
        team_project_id,
        extra={"operator": operator_id},
    )
    return True