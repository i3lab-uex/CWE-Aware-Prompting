# -*- coding: utf-8 -*-

"""
Access control module.

The `access_content` function determines whether a user is allowed to view
a particular piece of content based on their role and subscription level.
"""

from typing import Dict, Any

# Example user data. In a real system this would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

# Example content data. Each entry maps a content ID to the required
# subscription level and the actual payload.
CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"required_subscription": "bronze", "data": "Bronze content"},
    102: {"required_subscription": "silver", "data": "Silver content"},
    103: {"required_subscription": "gold", "data": "Gold content"},
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user is authorized.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access the content.
    content_id : int
        The ID of the content being requested.

    Returns
    -------
    Any
        The content data if authorized, otherwise the string 'Access Denied'.

    Notes
    -----
    - Admin users can access any content regardless of subscription level.
    - Regular users may only access content that matches *exactly* their
      subscription level.  This can be adjusted to allow higher tiers if
      desired.
    - If the user or content does not exist, access is denied to avoid leaking
      information.
    """
    # Fetch user and content safely; use .get() to avoid KeyError
    user = USERS.get(current_user_id)
    if not user:
        # Unknown user – deny access silently
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        # Unknown content – deny access silently
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["data"]

    # Regular users must have the exact required subscription
    if user.get("subscription") == content.get("required_subscription"):
        return content["data"]

    # All other cases are denied
    return "Access Denied"