from typing import Dict

# Example data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "tier": "premium"},
    2: {"role": "user",  "tier": "basic"},
    3: {"role": "user",  "tier": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced Python",   "required_tier": "premium"},
    102: {"title": "Intro to Python",   "required_tier": "basic"},
    103: {"title": "Data Science 101",  "required_tier": "premium"},
}

def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate user existence
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    # Validate content existence
    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users: check subscription tier
    user_tier = user.get("tier")
    required_tier = content.get("required_tier")

    # Simple tier hierarchy (basic < premium). Adjust as needed.
    tier_hierarchy = {"basic": 1, "premium": 2}

    if tier_hierarchy.get(user_tier, 0) >= tier_hierarchy.get(required_tier, 0):
        return content["title"]

    return "Access Denied"