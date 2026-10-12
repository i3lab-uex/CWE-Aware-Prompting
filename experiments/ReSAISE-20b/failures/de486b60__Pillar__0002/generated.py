# -*- coding: utf-8 -*-

"""
Access control module for content viewing.

The implementation follows the principle of least privilege and checks
the user role and subscription level before returning the requested
content title.  It is intentionally defensive against common access‑control
issues (CWE-284) by validating all inputs and explicitly denying any
request that does not meet the required criteria.
"""

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would come from a database or API.
# --------------------------------------------------------------------------- #

USERS = {
    # user_id : (role, subscription_level)
    1: ("admin", None),          # Administrators bypass all checks
    2: ("user", "basic"),
    3: ("user", "premium"),
    4: ("user", "free"),         # No content access
}

# The required subscription level for each piece of content.
# Lower string values imply stricter access (e.g., "basic" < "premium").
CONTENT = {
    101: ("Intro to Python", "free"),
    102: ("Advanced Python", "basic"),
    103: ("Data Science with Python", "premium"),
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_int(value: int, name: str) -> None:
    """
    Ensure that a value is an integer and within expected bounds.
    Raises ValueError if validation fails.
    """
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer.")

def _has_admin_access(user_role: str) -> bool:
    """
    Determine if the user has administrative privileges.
    """
    return user_role.lower() == "admin"

def _subscription_level_rank(level: str) -> int:
    """
    Convert a subscription level to an integer rank for comparison.
    Lower numbers mean higher privilege. Unknown levels are treated as
    the lowest possible rank (i.e., no access).
    """
    ranking = {"free": 0, "basic": 1, "premium": 2}
    return ranking.get(level.lower(), -1)

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized.
    
    Parameters
    ----------
    uid : int
        The ID of the user attempting to access the content.
    cont_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise "Access Denied".
    
    Raises
    ------
    KeyError
        If the user ID or content ID does not exist in the system.
    TypeError, ValueError
        If the provided arguments are of incorrect type or invalid value.
    """
    # Input validation
    _validate_int(uid, "uid")
    _validate_int(cont_id, "cont_id")

    # Retrieve user and content data
    try:
        user_role, user_level = USERS[uid]
    except KeyError as exc:
        raise KeyError(f"User ID {uid} not found.") from exc

    try:
        content_title, required_level = CONTENT[cont_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {cont_id} not found.") from exc

    # Admins bypass all checks
    if _has_admin_access(user_role):
        return content_title

    # Non‑admin users must meet or exceed the required subscription level
    user_rank = _subscription_level_rank(user_level)
    required_rank = _subscription_level_rank(required_level)

    if user_rank >= required_rank and user_rank != -1:
        return content_title

    # Deny access for all other cases
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Expected: "Intro to Python"
    print(view_content(2, 101))
    # Expected: "Access Denied" (free user accessing premium content)
    print(view_content(4, 103))
    # Expected: "Data Science with Python" (admin access)
    print(view_content(1, 103))