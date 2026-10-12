# -*- coding: utf-8 -*-
"""
Utility to retrieve content titles based on user permissions.

The module defines two global dictionaries:

USERS   : mapping of user_id -> dict(role, subscription)
CONTENT : mapping of content_id -> dict(title, required_subscription)

The function `retrieve_content` checks whether a user is allowed to view
a particular piece of content.  Administrators (role == 'admin') have
unrestricted access, while regular users must have a subscription level
equal to or higher than the required level for the content.
"""

from typing import Dict, Any

# Example data – replace with actual application data
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": None},
    2: {"role": "user", "subscription": "premium"},
    3: {"role": "user", "subscription": "basic"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Premium Article", "required_subscription": "premium"},
    102: {"title": "Basic Guide", "required_subscription": "basic"},
    103: {"title": "Exclusive Video", "required_subscription": "vip"},
}

# Define an ordering for subscription tiers to compare levels
SUBSCRIPTION_ORDER = {
    "basic": 1,
    "premium": 2,
    "vip": 3,
}


def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    user_id : int
        Identifier of the requesting user.
    content_id : int
        Identifier of the desired content.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Notes
    -----
    * Administrators have unrestricted access.
    * For regular users, the user's subscription level must be
      greater than or equal to the content's required level.
    * Missing user or content records result in 'Access Denied'.
    """
    # Validate input types
    if not isinstance(user_id, int) or not isinstance(content_id, int):
        return "Access Denied"

    # Retrieve user and content records
    user = USERS.get(user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users – check subscription tier
    user_sub = user.get("subscription")
    content_req = content.get("required_subscription")

    # If either subscription level is missing, deny access
    if user_sub not in SUBSCRIPTION_ORDER or content_req not in SUBSCRIPTION_ORDER:
        return "Access Denied"

    if SUBSCRIPTION_ORDER[user_sub] >= SUBSCRIPTION_ORDER[content_req]:
        return content["title"]

    # Default denial
    return "Access Denied"