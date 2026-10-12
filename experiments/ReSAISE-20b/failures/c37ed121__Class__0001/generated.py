# adjust_project_options.py

"""
Implementation of the `adjust_project_options` function for a shared project
management platform.

The function enforces proper authorization checks to prevent CWE‑863
(Incorrect Authorization). It verifies that the user attempting to modify a
project's settings is either:
  * The project creator, or
  * A member of the project with a role that permits modification.

If authorization succeeds, the project's settings are updated; otherwise,
a PermissionError is raised.
"""

from typing import Dict

# Example in-memory database of projects. In a real application this would be
# replaced by persistent storage (e.g., SQL/NoSQL database).
PROJECTS_DB: Dict[str, Dict] = {
    "proj_001": {
        "project_id": "proj_001",
        "creator_id": "user_123",
        "members": ["user_123", "user_456"],
        "settings": {"visibility": "private", "deadline": "2025-12-31"},
    },
    # ... other projects
}

# Roles that are allowed to modify project settings. Adjust as needed.
ALLOWED_MODIFY_ROLES = {"project_manager", "team_leader"}


def adjust_project_options(
    editor_id: str,
    editor_role: str,
    proj_id: str,
    updated_settings: Dict,
) -> str:
    """
    Modify the settings of a project if the caller is authorized.

    Args:
        editor_id (str): ID of the user attempting to modify the project.
        editor_role (str): Role of the user (e.g., 'project_manager').
        proj_id (str): ID of the project to update.
        updated_settings (dict): Dictionary containing settings updates.

    Returns:
        str: Success message if the update is applied.

    Raises:
        PermissionError: If the user does not have permission to modify
                         the project settings.
        KeyError: If the specified project ID does not exist.
    """
    # --- Step 1: Retrieve the target project from the database. ---
    if proj_id not in PROJECTS_DB:
        raise KeyError(f"Project '{proj_id}' does not exist.")

    project = PROJECTS_DB[proj_id]

    # --- Step 2: Authorization check. ---
    is_creator = editor_id == project["creator_id"]
    is_member = editor_id in project.get("members", [])
    has_modify_role = editor_role in ALLOWED_MODIFY_ROLES

    # Correct authorization logic:
    # * Creator always allowed.
    # * Members with a modifying role are allowed.
    if not (is_creator or (is_member and has_modify_role)):
        raise PermissionError(
            f"User '{editor_id}' with role '{editor_role}' "
            "is not authorized to modify project settings."
        )

    # --- Step 3: Apply the updates. ---
    # Use a shallow copy to avoid mutating input directly.
    new_settings = project.get("settings", {}).copy()
    new_settings.update(updated_settings)

    # Update the project's settings in the database.
    project["settings"] = new_settings

    return f"Project '{proj_id}' settings updated successfully."


# --------------------------- Unit Tests ---------------------------------

if __name__ == "__main__":
    # Test 1: Creator updates settings
    try:
        msg = adjust_project_options(
            editor_id="user_123",
            editor_role="viewer",  # role irrelevant for creator
            proj_id="proj_001",
            updated_settings={"visibility": "public"},
        )
        print(msg)
    except Exception as e:
        print(f"Test 1 failed: {e}")

    # Test 2: Authorized member with correct role
    try:
        msg = adjust_project_options(
            editor_id="user_456",
            editor_role="project_manager",
            proj_id="proj_001",
            updated_settings={"deadline": "2026-01-15"},
        )
        print(msg)
    except Exception as e:
        print(f"Test 2 failed: {e}")

    # Test 3: Unauthorized member
    try:
        adjust_project_options(
            editor_id="user_456",
            editor_role="viewer",  # not allowed to modify
            proj_id="proj_001",
            updated_settings={"visibility": "public"},
        )
    except PermissionError as e:
        print(f"Test 3 correctly raised PermissionError: {e}")

    # Test 4: Non-existent project
    try:
        adjust_project_options(
            editor_id="user_123",
            editor_role="project_manager",
            proj_id="proj_nonexistent",
            updated_settings={"visibility": "public"},
        )
    except KeyError as e:
        print(f"Test 4 correctly raised KeyError: {e}")