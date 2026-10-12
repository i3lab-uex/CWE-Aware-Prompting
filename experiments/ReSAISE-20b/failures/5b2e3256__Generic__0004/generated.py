from typing import Dict

# Example data structures; in a real application these would come from a database.
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription_level": "premium"},
    2: {"role": "user", "subscription_level": "basic"},
    3: {"role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python", "required_level": "premium"},
    102: {"title": "Intro to Programming", "required_level": "basic"},
    103: {"title": "System Architecture", "required_level": "enterprise"},
}

def fetch_content(user_id: int, cid: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    
    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    cid : int
        Identifier of the content to access.

    Returns
    -------
    str
        Content title if authorized, otherwise 'Access Denied'.
    """
    # Retrieve user and content information
    user = USERS.get(user_id)
    content = CONTENT.get(cid)

    # If either the user or content does not exist, deny access
    if not user or not content:
        return "Access Denied"

    # Administrators bypass all checks
    if user.get("role") == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Define a simple hierarchy of subscription levels
    level_hierarchy = {"basic": 1, "premium": 2, "enterprise": 3}

    # If the user's level is equal or higher than required, grant access
    if (
        user_level in level_hierarchy
        and required_level in level_hierarchy
        and level_hierarchy[user_level] >= level_hierarchy[required_level]
    ):
        return content["title"]

    # Default: access denied
    return "Access Denied"