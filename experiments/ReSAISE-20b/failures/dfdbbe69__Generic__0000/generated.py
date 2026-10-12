# -*- coding: utf-8 -*-

"""
Project membership management module.

This module provides the `handle_project_membership` function which allows
project owners to add or remove members from their own projects.  System
administrators have the privilege to modify any project.

The data model consists of two global dictionaries:

* `USERS`: maps user_id to a dictionary containing the user's role
  (`'admin'` or `'user'`).
* `PROJECTS`: maps project_id to a dictionary containing the project's
  owner (`owner_id`) and a set of member ids (`members`).

The function returns `True` on success, otherwise `False`.  No exception
is raised for expected error conditions; an exception is only raised if
an unexpected situation occurs (e.g. missing global data structures).
"""

from __future__ import annotations
from typing import Dict, Set

# --------------------------------------------------------------------------- #
# Example data structures (replace with real persistence in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin"},
    2: {"role": "user"},
    3: {"role": "user"},
    4: {"role": "user"},
}

PROJECTS: Dict[int, Dict[str, object]] = {
    101: {"owner_id": 2, "members": {3}},
    102: {"owner_id": 4, "members": set()},
}

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def handle_project_membership(
    req_user_id: int,
    proj_id: int,
    mod: str,
    mod_user_id: int
) -> bool:
    """
    Modify the membership of a project.

    Parameters
    ----------
    req_user_id : int
        The user performing the operation.
    proj_id : int
        Identifier of the project to modify.
    mod : str
        Either `'add'` or `'remove'`.
    mod_user_id : int
        Identifier of the user to add or remove.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, otherwise ``False``.

    Notes
    -----
    * Only a project owner or an administrator can modify membership.
    * The target user (`mod_user_id`) must exist in the system.
    * Adding an already existing member or removing a non‑member is
      considered a no‑op and still returns ``True``.
    """
    # Validate modification type
    if mod not in {"add", "remove"}:
        return False

    # Verify that the project exists
    project = PROJECTS.get(proj_id)
    if not project:
        return False

    # Verify that the target user exists
    if mod_user_id not in USERS:
        return False

    # Verify that the requesting user exists
    requester = USERS.get(req_user_id)
    if not requester:
        return False

    # Permission check: admin or owner
    is_admin = requester.get("role") == "admin"
    is_owner = project.get("owner_id") == req_user_id
    if not (is_admin or is_owner):
        return False

    # Ensure members is a set for idempotent operations
    members: Set[int] = project.setdefault("members", set())

    if mod == "add":
        members.add(mod_user_id)
    else:  # mod == "remove"
        members.discard(mod_user_id)

    return True

# --------------------------------------------------------------------------- #
# End of module
# --------------------------------------------------------------------------- #