# -*- coding: utf-8 -*-
"""
Project membership handler.

This module implements the `handle_project_membership` function which allows
project owners to add or remove members from their own projects, while users
with an admin role can modify any project.

The implementation follows the principle of least privilege and guards against
CWE‑284 (Improper Access Control) by explicitly checking the caller’s role
and ownership before performing any modifications.
"""

from typing import Dict

# Example data structures. In a real application these would be loaded from
# persistent storage (database, cache, etc.).
PROJECTS: Dict[int, Dict[str, any]] = {
    # project_id: { 'owner_id': int, 'members': set[int] }
}

USERS: Dict[int, str] = {
    # user_id: role ('admin' or 'user')
}


def handle_project_membership(
        req_user_id: int,
        proj_id: int,
        mod: str,
        mod_user_id: int
) -> bool:
    """
    Modify project membership.

    Parameters
    ----------
    req_user_id : int
        ID of the user performing the operation.
    proj_id : int
        Project identifier to be modified.
    mod : str
        Either 'add' or 'remove'.
    mod_user_id : int
        ID of the user to be added or removed.

    Returns
    -------
    bool
        True if operation succeeded, False otherwise.
    """
    # Validate modifier action
    if mod not in {"add", "remove"}:
        return False

    # Retrieve caller role
    req_role = USERS.get(req_user_id)
    if not req_role:
        return False  # unknown user

    # Retrieve project
    project = PROJECTS.get(proj_id)
    if not project:
        return False  # unknown project

    owner_id = project.get("owner_id")
    members = project.setdefault("members", set())

    # Authorization check
    if req_role != "admin" and req_user_id != owner_id:
        return False  # insufficient privileges

    if mod == "add":
        # No-op if already a member
        if mod_user_id in members:
            return True
        # Prevent adding non‑existent users
        if mod_user_id not in USERS:
            return False
        members.add(mod_user_id)
    else:  # mod == "remove"
        if mod_user_id not in members:
            return True  # nothing to do
        # Prevent removing the owner (unless caller is admin)
        if mod_user_id == owner_id and req_role != "admin":
            return False
        members.remove(mod_user_id)

    # Persist changes (in this example the in‑memory dict is already updated)
    return True