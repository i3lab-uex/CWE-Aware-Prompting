from typing import Dict, Any

# Example data structures (these would normally be loaded from a database or config)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription_level": 3},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_level": 1},
    102: {"title": "Premium Video", "required_level": 2},
    103: {"title": "Admin Guide", "required_level": 3},
}


def grant_access(user_id: int, item_id: int) -> str:
    """
    Determines whether a user is allowed to access a piece of content.

    Parameters
    ----------
    user_id : int
        Identifier for the requesting user.
    item_id : int
        Identifier for the content being requested.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Notes
    -----
    - Admin users (role == 'admin') are granted access to all content.
    - Regular users must have a subscription_level that is greater than or equal
      to the content's required_level.
    - If either the user_id or item_id is unknown, access is denied.
    """
    # Fetch user and content safely
    user = USERS.get(user_id)
    content = CONTENT.get(item_id)

    if not user or not content:
        # Unknown user or content – deny access
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: compare subscription levels
    user_level = user.get("subscription_level", 0)
    required_level = content.get("required_level", float("inf"))

    if user_level >= required_level:
        return content["title"]

    # All other cases: deny
    return "Access Denied"