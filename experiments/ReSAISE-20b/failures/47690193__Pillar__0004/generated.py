# -*- coding: utf-8 -*-
"""
Project permission management module.

This module defines a single function `control_project_permissions` that
enforces access control rules for modifying project memberships.  The
implementation follows the principle of least privilege: only an
administrator or the project owner may add or remove members.  All checks
are performed in a defensive manner to avoid inadvertent privilege
exposure (CWE‑284).

The module relies on two global dictionaries:

- `PROJECTS`: Mapping of project IDs to a dictionary containing at least
  the keys ``owner_id`` and ``members``.
- `USERS`: Mapping of user IDs to a dictionary containing at least
  the key ``role`` with possible values ``'admin'`` or ``'user'``.

Both dictionaries are assumed to be populated elsewhere in the
application.  The function does **not** raise exceptions for normal
failure conditions; it returns ``False`` instead.
"""

from __future__ import annotations

from typing import Dict, List, Any


# Example global data structures (replace with actual application data)
PROJECTS: Dict[int, Dict[str, Any]] = {
    1: {"owner_id": 10, "members": [20, 30]},
    2: {"owner_id": 11, "members": [40]},
}
USERS: Dict[int, Dict[str, str]] = {
    10: {"role": "user"},
    11: {"role": "admin"},
    20: {"role": "user"},
    30: {"role": "user"},
    40: {"role": "user"},
}


def control_project_permissions(
    executing_user_id: int,
    prjct_id: int,
    act_type: str,
    tgt_user_id: int,
) -> bool:
    """
    Add or remove a member from a project.

    Parameters
    ----------
    executing_user_id : int
        ID of the user performing the action.
    prjct_id : int
        Project identifier whose membership is to be modified.
    act_type : str
        Either ``'add'`` or ``'remove'``.
    tgt_user_id : int
        ID of the user being added or removed.

    Returns
    -------
    bool
        ``True`` if the operation succeeded, ``False`` otherwise.
    """
    # Validate action type
    if act_type not in {"add", "remove"}:
        return False

    # Retrieve executing user role
    exec_user = USERS.get(executing_user_id)
    if not exec_user:
        # Unknown executing user
        return False
    role = exec_user.get("role")
    if role not in {"admin", "user"}:
        return False

    # Retrieve target user existence
    if tgt_user_id not in USERS:
        return False

    # Retrieve project details
    project = PROJECTS.get(prjct_id)
    if not project:
        return False

    # Enforce access control
    is_owner = project.get("owner_id") == executing_user_id
    if role != "admin" and not is_owner:
        # Non-admin non-owner cannot modify membership
        return False

    members: List[int] = project.get("members", [])
    if act_type == "add":
        if tgt_user_id in members:
            # Already a member; no change required
            return True
        members.append(tgt_user_id)
    else:  # act_type == "remove"
        if tgt_user_id not in members:
            # Not a member; nothing to remove
            return True
        members.remove(tgt_user_id)

    # Persist the updated list back to the project record
    project["members"] = members
    return True


# Example usage (for testing purposes)
if __name__ == "__main__":
    assert control_project_permissions(10, 1, "add", 40) is True
    assert 40 in PROJECTS[1]["members"]
    assert control_project_permissions(20, 1, "remove", 30) is False