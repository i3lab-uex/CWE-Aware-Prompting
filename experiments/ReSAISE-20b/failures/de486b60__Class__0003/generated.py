# view_content.py

from typing import Dict, Any


# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_level": "basic"},
    102: {"title": "Premium Video", "required_level": "premium"},
    103: {"title": "Admin Guide", "required_level": "admin"},
}


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has sufficient
    permissions; otherwise return 'Access Denied'.

    Parameters
    ----------
    uid : int
        The ID of the user attempting to access content.
    cont_id : int
        The ID of the content the user wants to view.

    Returns
    -------
    str
        Content title if authorized, else 'Access Denied'.
    """
    # Verify user exists
    user = USERS.get(uid)
    if not user:
        return "Access Denied"

    # Verify content exists
    content = CONTENT.get(cont_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription level
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Define a simple level hierarchy
    levels = {"basic": 1, "premium": 2, "admin": 3}

    # If required level is not defined or unknown, deny
    if required_level not in levels:
        return "Access Denied"

    # If user level meets or exceeds required level, grant access
    if levels.get(user_level, 0) >= levels[required_level]:
        return content["title"]

    return "Access Denied"