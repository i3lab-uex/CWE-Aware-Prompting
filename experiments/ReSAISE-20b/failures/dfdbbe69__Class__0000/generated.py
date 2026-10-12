import typing as _t

# --------------------------------------------------------------------------- #
# Mock data structures – in a real application these would come from a DB
# --------------------------------------------------------------------------- #

PROJECTS: dict[int, dict[str, _t.Any]] = {
    # project_id : {"owner_id": int, "members": set[int]}
}

USERS: dict[int, dict[str, _t.Any]] = {
    # user_id : {"role": "admin" | "user"}
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user_role(user_id: int) -> str:
    """Return the role of a user. Raises KeyError if user does not exist."""
    return USERS[user_id]["role"]

def _is_admin(user_id: int) -> bool:
    """Return True if the user has an admin role."""
    return _get_user_role(user_id) == "admin"

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Modify the membership list of a project.

    Parameters
    ----------
    req_user_id : int
        The user performing the operation.
    proj_id : int
        Identifier of the target project.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        The user to be added/removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.

    Raises
    ------
    KeyError
        If any of the provided user or project IDs are not known.
    ValueError
        If `mod` is not one of 'add' or 'remove'.
    """
    # ----------------------------------------------------------------------- #
    # Validation & Authorization
    # ----------------------------------------------------------------------- #

    if proj_id not in PROJECTS:
        raise KeyError(f"Project {proj_id} does not exist")

    if req_user_id not in USERS:
        raise KeyError(f"Requester user {req_user_id} does not exist")

    if mod_user_id not in USERS:
        raise KeyError(f"Target user {mod_user_id} does not exist")

    if mod not in {"add", "remove"}:
        raise ValueError(f"Invalid operation '{mod}'. Must be 'add' or 'remove'")

    project = PROJECTS[proj_id]
    owner_id: int = project["owner_id"]
    members: set[int] = project.get("members", set())

    # Only the owner or an admin can modify membership
    if not (_is_admin(req_user_id) or req_user_id == owner_id):
        return False

    # ----------------------------------------------------------------------- #
    # Perform the operation
    # ----------------------------------------------------------------------- #

    if mod == "add":
        if mod_user_id in members:
            return False  # already a member
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return False  # cannot remove non‑member
        members.remove(mod_user_id)

    # Persist changes (in this mock setup we modify the dict in place)
    project["members"] = members
    return True

# --------------------------------------------------------------------------- #
# Example usage (commented out)
# --------------------------------------------------------------------------- #
"""
USERS = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"}
}
PROJECTS = {
    101: {"owner_id": 2, "members": {3}}
}

# Admin adds user 1 to project 101
assert handle_project_membership(1, 101, "add", 1) is True

# Non‑owner non‑admin tries to remove a member
assert handle_project_membership(3, 101, "remove", 2) is False
"""