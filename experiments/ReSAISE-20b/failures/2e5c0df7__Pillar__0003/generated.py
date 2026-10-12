# get_content.py

"""
Implements user access control for content based on subscription tier.
"""

from typing import Dict, Any

# Example data structures (replace with real data in production)
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, tier: int}
    1: {"role": "admin", "tier": 3},
    2: {"role": "user", "tier": 1},
    3: {"role": "user", "tier": 2},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_tier: int}
    101: {"title": "Intro to Python", "required_tier": 1},
    102: {"title": "Advanced Algorithms", "required_tier": 2},
    103: {"title": "Enterprise Architecture", "required_tier": 3},
}

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Returns the title of the requested content if the user has permission.
    Otherwise returns 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title if access granted, otherwise 'Access Denied'.
    """
    try:
        # Retrieve user and content records
        user = USERS[active_user_id]
        content_item = CONTENT[item_id]

        # Admins bypass tier checks
        if user.get("role") == "admin":
            return content_item["title"]

        # Regular users must meet or exceed required tier
        user_tier = int(user.get("tier", 0))
        required_tier = int(content_item.get("required_tier", 0))

        if user_tier >= required_tier:
            return content_item["title"]
    except (KeyError, TypeError, ValueError):
        # Missing user/content or invalid data leads to denial
        pass

    return "Access Denied"