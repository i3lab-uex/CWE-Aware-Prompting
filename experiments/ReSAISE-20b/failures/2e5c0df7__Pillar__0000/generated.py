# -*- coding: utf-8 -*-
"""
Utility module for content access control.
"""

from typing import Dict

# --------------------------------------------------------------------------- #
# Sample data structures (replace with actual data in production)
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    # user_id : {role: 'admin'|'user', subscription: 'basic'|'premium'|'enterprise'}
    1: {"role": "admin", "subscription": "enterprise"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    # content_id : {title: str, required_subscription: str}
    101: {"title": "Public Guide", "required_subscription": "basic"},
    102: {"title": "Advanced Tutorial", "required_subscription": "premium"},
    103: {"title": "Enterprise Overview", "required_subscription": "enterprise"},
}

# --------------------------------------------------------------------------- #
# Subscription hierarchy (higher index = higher tier)
# --------------------------------------------------------------------------- #

SUBSCRIPTION_LEVELS = ["basic", "premium", "enterprise"]


def _subscription_index(level: str) -> int:
    """
    Convert a subscription level to its numeric index.
    Raises KeyError if the level is unknown.
    """
    return SUBSCRIPTION_LEVELS.index(level)


def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the content title if the user is authorized, otherwise 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        Identifier of the user attempting to access content.
    item_id : int
        Identifier of the requested content.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Notes
    -----
    - Administrators have unrestricted access.
    - Regular users must meet or exceed the required subscription level.
    - Unknown user or content IDs result in 'Access Denied'.
    """
    # Retrieve user record
    user = USERS.get(active_user_id)
    if not user:
        return "Access Denied"

    # Admin users bypass checks
    if user.get("role") == "admin":
        content = CONTENT.get(item_id)
        return content["title"] if content else "Access Denied"

    # Regular user access control
    required = CONTENT.get(item_id)
    if not required:
        return "Access Denied"

    try:
        user_level = _subscription_index(user["subscription"])
        required_level = _subscription_index(required["required_subscription"])
    except (KeyError, ValueError):
        # Invalid subscription level
        return "Access Denied"

    if user_level >= required_level:
        return required["title"]
    else:
        return "Access Denied"