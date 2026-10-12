# -*- coding: utf-8 -*-
"""
Secure content retrieval based on user role and subscription level.

The module defines:
    - USERS: mapping of user_id -> dict(role, subscription)
    - CONTENT: mapping of content_id -> dict(title, required_subscription)
    - SUBSCRIPTION_HIERARCHY: ordered list of subscription levels
    - retrieve_content(): the function requested in the specification
"""

from __future__ import annotations

# ----------------------------------------------------------------------
# Sample data (in a real application these would come from a database)
# ----------------------------------------------------------------------
USERS: dict[int, dict[str, str]] = {
    1: {"role": "admin", "subscription": "premium"},
    2: {"role": "user", "subscription": "basic"},
    3: {"role": "user", "subscription": "premium"},
}

CONTENT: dict[int, dict[str, str]] = {
    101: {"title": "Public Article", "required_subscription": "basic"},
    102: {"title": "Premium Video", "required_subscription": "premium"},
    103: {"title": "Admin Report", "required_subscription": "enterprise"},
}

SUBSCRIPTION_HIERARCHY: list[str] = ["basic", "premium", "enterprise"]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _subscription_index(level: str) -> int:
    """
    Return the index of a subscription level in the hierarchy.
    If level is not found, return -1 (treated as lowest).
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError:
        return -1

def _has_access(user_sub: str, content_req: str) -> bool:
    """
    Determine if a user with subscription `user_sub` can access
    content requiring `content_req`.
    """
    return _subscription_index(user_sub) >= _subscription_index(content_req)

# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user requesting access.
    contid : int
        Identifier of the content to be retrieved.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Validate user exists
    user = USERS.get(usr_id)
    if not user:
        return "Access Denied"

    # Validate content exists
    content = CONTENT.get(contid)
    if not content:
        return "Access Denied"

    # Admins bypass subscription checks
    if user.get("role") == "admin":
        return content["title"]

    # Regular users must satisfy subscription requirement
    if _has_access(user.get("subscription", ""), content["required_subscription"]):
        return content["title"]

    return "Access Denied"

# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    print(retrieve_content(1, 102))  # Admin: should succeed
    print(retrieve_content(2, 102))  # Basic user: should fail
    print(retrieve_content(3, 102))  # Premium user: should succeed