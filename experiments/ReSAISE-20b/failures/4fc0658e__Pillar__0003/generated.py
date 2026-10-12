# -*- coding: utf-8 -*-

"""
A simple access control module that demonstrates how to restrict content
access based on user roles and subscription levels.
"""

# Example data – in a real application these would come from a database
USERS = {
    1: {"user_id": 1, "role": "admin", "subscription_level": "premium"},
    2: {"user_id": 2, "role": "user",  "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user",  "subscription_level": "premium"},
}

CONTENT = {
    101: {"title": "Intro to Python",   "required_level": "basic"},
    102: {"title": "Advanced AI",       "required_level": "premium"},
    103: {"title": "Admin Secrets",     "required_level": "admin"},   # only admins
}

# Define the hierarchy of subscription levels for comparison
LEVEL_HIERARCHY = {"basic": 1, "premium": 2, "admin": 3}


def fetch_content(given_user_id: int, target_content_id: int) -> str:
    """
    Return the title of the requested content if the user is authorized,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    given_user_id : int
        Identifier of the user attempting to access the content.
    target_content_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title if access is granted, else 'Access Denied'.
    """
    # Validate input types
    if not isinstance(given_user_id, int) or not isinstance(target_content_id, int):
        raise TypeError("User ID and Content ID must be integers")

    # Fetch user record
    user = USERS.get(given_user_id)
    if not user:
        return "Access Denied"

    # Fetch content record
    content = CONTENT.get(target_content_id)
    if not content:
        return "Access Denied"

    # Admins have full access
    if user["role"] == "admin":
        return content["title"]

    # For regular users, compare subscription levels
    user_level = LEVEL_HIERARCHY.get(user["subscription_level"])
    content_level = LEVEL_HIERARCHY.get(content["required_level"])

    # If the required level is not recognized, deny access
    if content_level is None:
        return "Access Denied"

    # Users can access content if their level is equal or higher
    if user_level >= content_level:
        return content["title"]

    # All other cases result in denial
    return "Access Denied"