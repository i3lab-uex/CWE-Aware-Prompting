# -*- coding: utf-8 -*-
"""
Project access management module.

This module defines a single function `manage_project_access` that allows
project owners to add or remove members from their project.  Users with the
role `admin` can modify any project.

The module expects two global dictionaries to be defined in the importing
context:

    PROJECTS: dict[int, dict[str, Any]]
        Mapping from project_id to a dictionary that must contain the keys
        `owner_id` (int) and `members` (set[int]).

    USERS: dict[int, dict[str, Any]]
        Mapping from user_id to a dictionary that must contain the key
        `role` (str).  The role string may be `'admin'`, `'owner'`,
        `'member'`, etc.

If these dictionaries are missing or the required keys are absent, the
function will raise a `KeyError` with an informative message.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user_role(user_id: int) -> str:
    """
    Retrieve the role of a user from the USERS dictionary.

    Parameters
    ----------
    user_id : int
        The ID of the user whose role is requested.

    Returns
    -------
    str
        The role string associated with the user.

    Raises
    ------
    KeyError
        If the user_id is not present in USERS.
    """
    try:
        return USERS[user_id]["role"]
    except KeyError as exc:
        raise KeyError(f"User ID {user_id} not found in USERS.") from exc


def _get_project(project_id: int) -> dict[str, Any]:
    """
    Retrieve the project dictionary from the PROJECTS mapping.

    Parameters
    ----------
    project_id : int
        The ID of the project to retrieve.

    Returns
    -------
    dict[str, Any]
        The dictionary representing the project.

    Raises
    ------
    KeyError
        If the project_id is not present in PROJECTS.
    """
    try:
        return PROJECTS[project_id]
    except KeyError as exc:
        raise KeyError(f"Project ID {project_id} not found in PROJECTS.") from exc


# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def manage_project_access(
    current_user_id: int,
    project_id: int,
    action: str,
    target_user_id: int
) -> bool:
    """
    Add or remove a member from a project.

    Only the owner of the project or an admin user can perform this action.
    The function returns ``True`` if the operation succeeds, otherwise
    ``False``.

    Parameters
    ----------
    current_user_id : int
        The ID of the user invoking the function.
    project_id : int
        The ID of the project to modify.
    action : str
        Either ``'add'`` or ``'remove'``.  Case-insensitive.
    target_user_id : int
        The ID of the user to add or remove.

    Returns
    -------
    bool
        ``True`` if the modification was applied, otherwise ``False``.

    Raises
    ------
    KeyError
        If the project or user does not exist in their respective dictionaries.
    ValueError
        If an unsupported action is supplied.
    """
    # Normalise the action string to lower case
    act = action.lower()
    if act not in {"add", "remove"}:
        raise ValueError(f"Unsupported action '{action}'. Must be 'add' or 'remove'.")

    # Retrieve project and user role
    proj = _get_project(project_id)
    current_role = _get_user_role(current_user_id)

    # Permission check: admin or owner
    if current_role != "admin" and proj["owner_id"] != current_user_id:
        return False

    # Ensure the members set exists and is mutable
    if "members" not in proj or not isinstance(proj["members"], set):
        raise KeyError(f"Project {project_id} does not have a valid 'members' set.")

    members = proj["members"]

    if act == "add":
        # Avoid adding duplicate entries
        if target_user_id in members:
            return False  # No change needed
        members.add(target_user_id)
    else:  # act == "remove"
        if target_user_id not in members:
            return False  # Nothing to remove
        members.remove(target_user_id)

    return True


# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

# if __name__ == "__main__":
#     # Example global dictionaries
#     PROJECTS = {
#         1: {"owner_id": 10, "members": {20, 30}},
#         2: {"owner_id": 11, "members": {40}}
#     }
#     USERS = {
#         10: {"role": "owner"},
#         11: {"role": "admin"},
#         20: {"role": "member"},
#         30: {"role": "member"},
#         40: {"role": "member"}
#     }
#
#     print(manage_project_access(10, 1, 'add', 40))   # True
#     print(manage_project_access(11, 1, 'remove', 20)) # True
#     print(manage_project_access(30, 1, 'add', 50))    # False (not owner/admin)