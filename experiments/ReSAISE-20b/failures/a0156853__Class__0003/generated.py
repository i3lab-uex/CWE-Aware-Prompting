# -*- coding: utf-8 -*-
"""
Implementation of access control for content based on user role and subscription level.
"""

from typing import Dict, Any

# Example data structures (replace with real data sources in production)
USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Public Article", "required_level": None},
    102: {"content_id": 102, "title": "Basic Video", "required_level": "basic"},
    103: {"content_id": 103, "title": "Premium Podcast", "required_level": "premium"},
}


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user is allowed to access the requested content.

    Parameters
    ----------
    uid : int
        User ID of the requester.
    cid : int
        Content ID being requested.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise, 'Access Denied'.

    Notes
    -----
    - Admin users bypass subscription checks.
    - If the user or content does not exist, access is denied.
    - All inputs are validated for type and existence to mitigate CWE-862 (Missing Authorization).
    """
    # Validate that uid and cid are integers
    if not isinstance(uid, int) or not isinstance(cid, int):
        return "Access Denied"

    # Retrieve user and content records
    user = USERS.get(uid)
    content = CONTENT.get(cid)

    # If either record is missing, deny access
    if user is None or content is None:
        return "Access Denied"

    # Admins have unrestricted access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must have a subscription level
    user_level = user.get("subscription_level")
    if not isinstance(user_level, str):
        return "Access Denied"

    # Determine required level for the content
    required_level = content.get("required_level")

    # If content is public (no requirement), grant access
    if required_level is None:
        return content["title"]

    # If the user's level matches or exceeds the required level, grant access
    # Assuming a simple hierarchy: basic < premium
    hierarchy = {"basic": 1, "premium": 2}
    user_rank = hierarchy.get(user_level)
    required_rank = hierarchy.get(required_level)

    if user_rank is None or required_rank is None:
        return "Access Denied"

    if user_rank >= required_rank:
        return content["title"]

    # Otherwise, deny access
    return "Access Denied"