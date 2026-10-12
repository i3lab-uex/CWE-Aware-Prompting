# -*- coding: utf-8 -*-

from typing import Dict, Any

# Example user data structure
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": 1},
    3: {"user_id": 3, "role": "user", "subscription_level": 2},
}

# Example content data structure
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Basic Article", "required_level": 1},
    102: {"content_id": 102, "title": "Premium Video", "required_level": 2},
    103: {"content_id": 103, "title": "Admin Guide", "required_level": None},
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determine if a user is allowed to access a piece of content.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise
        'Access Denied'.

    Notes
    -----
    * Admin users have unrestricted access.
    * Regular users may only access content whose required subscription
      level is less than or equal to their own level.
    * If the user, content, or subscription data is missing, access is
      denied to avoid leaking information.
    """
    # Fetch user and content data safely
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(item_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content.get("title", "Access Denied")

    # Regular users: compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # If either level is None, deny access
    if user_level is None or required_level is None:
        return "Access Denied"

    # Enforce strict numeric comparison
    try:
        if int(user_level) >= int(required_level):
            return content.get("title", "Access Denied")
    except (ValueError, TypeError):
        # In case levels are not comparable
        return "Access Denied"

    return "Access Denied"