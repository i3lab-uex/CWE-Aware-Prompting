import typing as _t

# Example data structures; in real usage these would come from your database or API
PROJECTS: dict[int, dict[str, _t.Any]] = {
    1: {"owner_id": 10, "members": {20, 30}},
    2: {"owner_id": 11, "members": {21}},
}
USERS: dict[int, str] = {
    10: "admin",
    11: "user",
    20: "user",
    21: "user",
    30: "admin",
}


def control_project_participants(
    acting_user_id: int,
    prj_id: int,
    action_type: str,
    target_id: int,
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    acting_user_id : int
        The ID of the user performing the action.
    prj_id : int
        The project being modified.
    action_type : str
        Either 'add' or 'remove'.
    target_id : int
        The user ID to be added or removed.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    * Only a project owner or an administrator can modify participants.
    * Adding the same member twice or removing a non‑member is considered a failure.
    """
    # Basic type validation
    if not isinstance(acting_user_id, int) or not isinstance(prj_id, int):
        return False
    if action_type not in {"add", "remove"}:
        return False
    if not isinstance(target_id, int):
        return False

    # Verify that the project exists
    project = PROJECTS.get(prj_id)
    if not project:
        return False

    # Verify that the acting user exists
    role = USERS.get(acting_user_id)
    if role is None:
        return False

    # Permission check: admin can do anything; owner can modify own project
    if role != "admin" and acting_user_id != project.get("owner_id"):
        return False

    members = project.setdefault("members", set())

    if action_type == "add":
        # Avoid adding duplicates
        if target_id in members:
            return False
        members.add(target_id)
    else:  # remove
        if target_id not in members:
            return False
        members.remove(target_id)

    return True