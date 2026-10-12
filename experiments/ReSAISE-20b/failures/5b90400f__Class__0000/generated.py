# -*- coding: utf-8 -*-

"""
Access control module for content delivery.

The function `access_content` enforces that only users with the appropriate
subscription level or an admin role may retrieve a piece of content.
"""

from typing import Dict, Any

# Example user and content databases
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription: str}
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {level_required: str, data: str}
    101: {"level_required": "bronze", "data": "Basic Content"},
    102: {"level_required": "silver", "data": "Intermediate Content"},
    103: {"level_required": "gold",   "data": "Premium Content"},
}


def _get_user(user_id: int) -> Dict[str, Any]:
    """
    Retrieve user information from the USERS dictionary.
    Raises KeyError if the user is not found.
    """
    return USERS[user_id]


def _get_content(content_id: int) -> Dict[str, Any]:
    """
    Retrieve content information from the CONTENT dictionary.
    Raises KeyError if the content is not found.
    """
    return CONTENT[content_id]


def _subscription_level_hierarchy() -> Dict[str, int]:
    """
    Define a numeric hierarchy for subscription levels.
    Higher numbers indicate higher access rights.
    """
    return {"bronze": 1, "silver": 2, "gold": 3}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user is authorized.
    If the user does not exist, or the content does not exist,
    raise a KeyError.  If authorization fails, return
    'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        Identifier of the user attempting access.
    content_id : int
        Identifier of the requested content.

    Returns
    -------
    Any
        The content data if authorized, otherwise the string 'Access Denied'.

    Raises
    ------
    KeyError
        If either user or content is not found in the respective dictionaries.
    """
    # Retrieve entities
    user = _get_user(current_user_id)
    content = _get_content(content_id)

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["data"]

    # Normal users must meet or exceed the required level
    hierarchy = _subscription_level_hierarchy()
    user_level_value = hierarchy.get(user["subscription"], 0)
    required_level_value = hierarchy.get(content["level_required"], 0)

    if user_level_value >= required_level_value:
        return content["data"]

    # Authorization failed
    return "Access Denied"


# Example usage (uncomment to test)
# if __name__ == "__main__":
#     print(access_content(2, 102))   # Intermediate Content
#     print(access_content(3, 103))   # Access Denied