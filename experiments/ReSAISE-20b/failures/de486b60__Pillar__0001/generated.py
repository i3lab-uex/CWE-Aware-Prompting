# view_content.py

from typing import Dict, Any

# Sample data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_level": "basic"},
    102: {"title": "Premium Guide", "required_level": "premium"},
    103: {"title": "Admin Handbook", "required_level": "admin"},
}

# Define a clear hierarchy of subscription levels
LEVEL_HIERARCHY = {
    "basic": 1,
    "premium": 2,
    "admin": 3,   # admin is the highest level
}


def _get_user_info(uid: int) -> Dict[str, Any]:
    """
    Retrieve user information securely.
    Raises KeyError if the user does not exist.
    """
    return USERS[uid]


def _get_content_info(cont_id: int) -> Dict[str, Any]:
    """
    Retrieve content information securely.
    Raises KeyError if the content does not exist.
    """
    return CONTENT[cont_id]


def _has_access(user_level: str, content_level: str) -> bool:
    """
    Determine if a user with `user_level` can access content requiring
    `content_level`. Admins have universal access.
    """
    # Normalize levels
    user_rank = LEVEL_HIERARCHY.get(user_level.lower(), 0)
    content_rank = LEVEL_HIERARCHY.get(content_level.lower(), 0)

    # Admins can access everything
    if user_rank == LEVEL_HIERARCHY["admin"]:
        return True

    # Regular users can access content at or below their level
    return user_rank >= content_rank


def view_content(uid: int, cont_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters:
        uid (int): User ID attempting access.
        cont_id (int): Content ID requested.

    Returns:
        str: Title of the content or 'Access Denied'.
    """
    try:
        user = _get_user_info(uid)
        content = _get_content_info(cont_id)

        if _has_access(user["subscription_level"], content["required_level"]):
            return content["title"]
        else:
            return "Access Denied"

    except KeyError:
        # If user or content does not exist, treat as unauthorized
        return "Access Denied"