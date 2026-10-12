#!/usr/bin/env python3
"""
access_content.py

Provides a function to fetch content based on user subscription level.
"""

from typing import Any, Dict

# Example data structures – in a real system these would come from a database.
USERS: Dict[int, Dict[str, Any]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"title": "Basic Article", "required_subscription": "basic"},
    102: {"title": "Premium Video", "required_subscription": "premium"},
    103: {"title": "Admin Guide", "required_subscription": "admin"},  # special case
}


def access_content(current_user_id: int, content_id: int) -> Any:
    """
    Return the requested content if the user has permission, otherwise return 'Access Denied'.

    Parameters
    ----------
    current_user_id : int
        The ID of the user attempting to access the content.
    content_id : int
        The ID of the content item.

    Returns
    -------
    Any
        The content data dictionary if authorized, else the string 'Access Denied'.
    """
    # Validate input types
    if not isinstance(current_user_id, int) or not isinstance(content_id, int):
        return "Access Denied"

    # Fetch user and content safely
    user = USERS.get(current_user_id)
    if not user:
        return "Access Denied"

    content = CONTENT.get(content_id)
    if not content:
        return "Access Denied"

    # Admins bypass all checks
    if user.get("role") == "admin":
        return content

    # For regular users, check subscription level
    required = content.get("required_subscription")
    if not required:
        return "Access Denied"

    # If the content is marked for 'admin' only, deny non-admins
    if required == "admin":
        return "Access Denied"

    # Simple equality check – could be expanded to a hierarchy
    if user.get("subscription") == required:
        return content

    # No match – deny access
    return "Access Denied"


# Example usage (for testing purposes)
if __name__ == "__main__":
    print(access_content(1, 101))  # Admin accessing basic content
    print(access_content(2, 102))  # Basic user trying premium content
    print(access_content(3, 102))  # Premium user accessing premium content