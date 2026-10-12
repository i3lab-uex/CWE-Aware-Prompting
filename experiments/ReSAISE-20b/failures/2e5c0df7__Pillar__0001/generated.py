# -*- coding: utf-8 -*-
"""
Content access control module.

The function `get_content` checks whether a user has permission to view
a particular piece of content.  Administrators can access everything,
while regular users must have a subscription level that matches or
exceeds the content's required level.
"""

from typing import Dict

# Example data structures.  In a real system these would be populated from
# a database or other persistent store.
USERS: Dict[int, Dict[str, str | int]] = {
    # user_id : { "role": "admin" | "user", "subscription_level": int }
    1: {"role": "admin", "subscription_level": 3},
    2: {"role": "user", "subscription_level": 1},
    3: {"role": "user", "subscription_level": 2},
}

CONTENT: Dict[int, Dict[str, str | int]] = {
    # content_id : { "title": str, "required_level": int }
    101: {"title": "Public Article", "required_level": 0},
    102: {"title": "Premium Video", "required_level": 2},
    103: {"title": "VIP Interview", "required_level": 3},
}


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of a content item if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist.
    """
    # Retrieve user and content records.  Using .get() would hide missing
    # entries, which could be a security issue; raising KeyError is safer.
    try:
        user = USERS[active_user_id]
    except KeyError as exc:
        raise KeyError(f"User ID {active_user_id} not found.") from exc

    try:
        content = CONTENT[item_id]
    except KeyError as exc:
        raise KeyError(f"Content ID {item_id} not found.") from exc

    # Administrators bypass all checks.
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level >= required_level.
    user_level = int(user.get("subscription_level", 0))
    required_level = int(content.get("required_level", 0))

    if user_level >= required_level:
        return content["title"]

    # If none of the above, deny access.
    return "Access Denied"


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    print(get_content(1, 103))  # Admin: VIP Interview
    print(get_content(2, 102))  # User with level 1: Access Denied
    print(get_content(3, 102))  # User with level 2: Premium Video