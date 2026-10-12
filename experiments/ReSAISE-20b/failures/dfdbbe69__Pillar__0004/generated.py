import logging

# Sample data structures – in a real system these would be loaded from a database.
PROJECTS = {
    # project_id: {"owner_id": int, "members": set of user_ids}
}

USERS = {
    # user_id: {"role": "admin" | "user"}
}


def handle_project_membership(req_user_id: int, proj_id: int,
                              mod: str, mod_user_id: int) -> bool:
    """
    Allow project owners or admins to add/remove members from a project.

    Parameters
    ----------
    req_user_id : int
        The ID of the user performing the action.
    proj_id : int
        The project to modify.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        The user to add/remove.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate action type
    if mod not in {"add", "remove"}:
        logging.warning("Invalid modification type: %s", mod)
        return False

    # Retrieve project and user records
    project = PROJECTS.get(proj_id)
    if not project:
        logging.warning("Project %s does not exist.", proj_id)
        return False

    if mod_user_id not in USERS:
        logging.warning("Target user %s does not exist.", mod_user_id)
        return False

    # Check permissions: admin or owner
    requester = USERS.get(req_user_id)
    if not requester:
        logging.warning("Requester %s does not exist.", req_user_id)
        return False

    is_admin = requester.get("role") == "admin"
    is_owner = project["owner_id"] == req_user_id

    if not (is_admin or is_owner):
        logging.warning(
            "User %s lacks permission to modify project %s.",
            req_user_id, proj_id
        )
        return False

    members = project.setdefault("members", set())

    if mod == "add":
        # Idempotent: adding an existing member is a no-op but still success
        if mod_user_id in members:
            logging.info(
                "User %s already a member of project %s.", mod_user_id, proj_id
            )
        else:
            members.add(mod_user_id)
            logging.info(
                "User %s added to project %s by user %s.",
                mod_user_id, proj_id, req_user_id
            )
        return True

    # mod == "remove"
    if mod_user_id not in members:
        logging.warning(
            "User %s is not a member of project %s; cannot remove.",
            mod_user_id, proj_id
        )
        return False

    members.remove(mod_user_id)
    logging.info(
        "User %s removed from project %s by user %s.",
        mod_user_id, proj_id, req_user_id
    )
    return True