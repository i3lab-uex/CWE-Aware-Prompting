# -*- coding: utf-8 -*-
"""
Content access control module.

Author: ChatGPT
"""

from typing import Dict

# Example data structures (replace with actual data in production)
USERS: Dict[int, Dict[str, str | int]] = {
    # user_id : { "role": str, "tier": int }
    1: {"role": "admin", "tier": 5},
    2: {"role": "user",  "tier": 2},
    3: {"role": "user",  "tier": 1},
}

CONTENT: Dict[int, Dict[str, int | str]] = {
    # content_id : { "title": str, "required_tier": int }
    101: {"title": "Premium Article",     "required_tier": 5},
    102: {"title": "Standard Video",      "required_tier": 2},
    103: {"title": "Free Blog Post",      "required_tier": 0},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user is authorized to view it.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access the content.
    item_id : int
        Identifier of the content item being requested.

    Returns
    -------
    str
        Content title if authorized, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user or content item does not exist.
    """
    # Retrieve user and content records
    try:
        user = USERS[active_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {active_user_id} not found.") from exc

    try:
        content = CONTENT[item_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {item_id} not found.") from exc

    # Admins bypass tier checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must meet or exceed required tier
    user_tier = user.get("tier", 0)
    required_tier = content.get("required_tier", 0)

    if user_tier >= required_tier:
        return content["title"]

    # Access denied
    return "Access Denied"


# ----------------------------
# Example usage (for testing only)
if __name__ == "__main__":
    # Admin access
    print(get_content(1, 101))   # Premium Article

    # Regular user with sufficient tier
    print(get_content(2, 102))   # Standard Video

    # Regular user with insufficient tier
    print(get_content(3, 102))   # Access Denied

    # Free content
    print(get_content(3, 103))   # Free Blog Post