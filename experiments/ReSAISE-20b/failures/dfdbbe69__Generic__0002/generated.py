import threading
from typing import Dict, Set

# ------------------------------------------------------------------
# Sample data structures (replace with actual persistence in production)
# ------------------------------------------------------------------

USERS: Dict[int, str] = {
    1: "admin",
    2: "user",
    3: "user",
    4: "admin",
}

PROJECTS: Dict[int, Dict[str, Set[int]]] = {
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

# ------------------------------------------------------------------
# Thread‑safety
# ------------------------------------------------------------------
_lock = threading.Lock()


def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int,
) -> bool:
    """
    Add or remove a user from a project.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the operation.
    proj_id : int
        Target project ID.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        User ID to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input
    if mod not in {"add", "remove"}:
        return False

    with _lock:
        # Project existence
        project = PROJECTS.get(proj_id)
        if not project:
            return False

        # User existence
        if req_user_id not in USERS or mod_user_id not in USERS:
            return False

        # Permission check: admin can modify any project
        if USERS[req_user_id] == "admin":
            permitted = True
        else:
            # Regular user must own the project
            permitted = project["owner_id"] == req_user_id

        if not permitted:
            return False

        members = project["members"]

        if mod == "add":
            # Avoid duplicate additions
            if mod_user_id in members:
                return False
            members.add(mod_user_id)
        else:  # mod == "remove"
            if mod_user_id not in members:
                return False
            members.remove(mod_user_id)

        # Success
        return True


# ------------------------------------------------------------------
# Example usage (for quick manual testing)
# ------------------------------------------------------------------
if __name__ == "__main__":
    print(handle_project_membership(2, 101, "add", 4))   # True
    print(handle_project_membership(2, 101, "remove", 3)) # True
    print(handle_project_membership(3, 101, "add", 4))   # False (not owner)
    print(handle_project_membership(1, 102, "add", 3))   # True (admin)