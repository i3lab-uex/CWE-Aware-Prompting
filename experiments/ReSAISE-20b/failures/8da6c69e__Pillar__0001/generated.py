# Assume these global dictionaries are defined elsewhere in the application.
# For the sake of a self‑contained example, minimal mock data is provided here.

PROJECTS = {
    1: {"owner_id": 101, "members": {201, 202}},
    2: {"owner_id": 102, "members": {203}},
}

USERS = {
    101: "user",
    102: "user",
    201: "user",
    202: "user",
    203: "user",
    301: "admin",   # admin user
}

def handle_project_membership(
    acting_user_id: int,
    prjt_id: int,
    member_action: str,
    target_member_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    acting_user_id : int
        The user performing the action.
    prjt_id : int
        ID of the project to modify.
    member_action : str
        Either 'add' or 'remove'.
    target_member_id : int
        User ID of the member to add or remove.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate action string early to avoid accidental misuse
    if member_action not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(prjt_id)
    if not project:
        return False

    # Verify that the target member exists in the system
    if target_member_id not in USERS:
        return False

    # Determine whether the acting user is allowed to modify this project
    acting_role = USERS.get(acting_user_id)
    if acting_role == "admin":
        authorized = True
    else:
        # Non-admins can only modify projects they own
        authorized = (acting_user_id == project.get("owner_id"))

    if not authorized:
        return False

    # Perform the action
    members = project.setdefault("members", set())
    if member_action == "add":
        # Avoid adding duplicates; no-op if already present
        members.add(target_member_id)
    else:  # member_action == "remove"
        if target_member_id in members:
            members.remove(target_member_id)
        else:
            # Trying to remove a member who isn't part of the project
            return False

    # If we reach here, operation succeeded
    return True