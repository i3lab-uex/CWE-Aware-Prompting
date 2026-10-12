# -*- coding: utf-8 -*-

"""
Project access management module.

This module defines a single function, `manage_team_access`, which allows
project owners to modify the membership of their own projects and allows
administrators to modify any project.  The function performs explicit access
control checks to prevent unauthorized modifications, mitigating CWE-284
(Improper Access Control).

The module assumes the presence of two global dictionaries:

    PROJECTS: Mapping[int, dict] where each project dictionary contains:
        - 'owner_id': int
        - 'members': set[int]

    USERS: Mapping[int, str] where the value is either `'admin'` or `'user'`.
"""

from __future__ import annotations

# Example data structures; in real use these would be populated elsewhere.
PROJECTS: dict[int, dict[str, set[int] | int]] = {}
USERS: dict[int, str] = {}


def manage_team_access(
    executor_user_id: int,
    proj_id: int,
    operation: str,
    target_member_id: int
) -> bool:
    """
    Modify project membership.

    Parameters
    ----------
    executor_user_id : int
        The user performing the operation.
    proj_id : int
        Identifier of the target project.
    operation : str
        Either 'add' or 'remove'.
    target_member_id : int
        The user to be added or removed.

    Returns
    -------
    bool
        True if the operation succeeded, False otherwise.
    """
    # Validate input types early to avoid accidental injection or misuse
    if not isinstance(executor_user_id, int) \
       or not isinstance(proj_id, int) \
       or not isinstance(operation, str) \
       or not isinstance(target_member_id, int):
        return False

    # Ensure operation is one of the allowed actions
    if operation not in {"add", "remove"}:
        return False

    # Check that the project exists
    project = PROJECTS.get(proj_id)
    if project is None:
        return False

    # Verify that the target member exists in the user base
    if target_member_id not in USERS:
        return False

    # Retrieve executor role, defaulting to 'user' if unknown
    executor_role = USERS.get(executor_user_id, "user")

    # Authorization: admin can modify any project; owner can modify own
    if executor_role != "admin" and executor_user_id != project["owner_id"]:
        return False

    # Perform the requested operation
    members: set[int] = project["members"]

    if operation == "add":
        # Adding a member that is already present is harmless
        members.add(target_member_id)
    else:  # operation == "remove"
        # Removing a non‑existent member is also harmless
        members.discard(target_member_id)

    return True