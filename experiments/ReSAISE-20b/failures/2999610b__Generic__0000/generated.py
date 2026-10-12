# -*- coding: utf-8 -*-
"""
Utility module for content access control.
"""

from typing import Dict, Any

# ----------------------------------------------------------------------
# Example data structures (replace with real data in production)
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, Any]] = {
    # user_id : {role: str, subscription: str}
    1: {"role": "admin",   "subscription": "premium"},
    2: {"role": "user",    "subscription": "free"},
    3: {"role": "user",    "subscription": "basic"},
    4: {"role": "user",    "subscription": "premium"},
}

CONTENT: Dict[int, Dict[str, Any]] = {
    # content_id : {title: str, required_subscription: str}
    101: {"title": "Public Article",      "required_subscription": "free"},
    102: {"title": "Basic Tutorial",     "required_subscription": "basic"},
    103: {"title": "Premium Guide",      "required_subscription": "premium"},
    104: {"title": "Admin Only Doc",     "required_subscription": "admin"},
}

# Order of subscription levels from lowest to highest
SUBSCRIPTION_HIERARCHY = ["free", "basic", "premium"]

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def _get_subscription_rank(level: str) -> int:
    """
    Return the rank of a subscription level.
    Lower index means lower privilege.
    Raises ValueError if level is unknown.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError as exc:
        raise ValueError(f"Unknown subscription level: {level}") from exc


def _has_access(user_sub: str, content_req: str) -> bool:
    """
    Determine if a user with subscription `user_sub` can access content
    requiring subscription `content_req`.
    Administrators are handled separately.
    """
    # If content requires admin role, only admins can access
    if content_req == "admin":
        return False  # handled in main function

    try:
        user_rank = _get_subscription_rank(user_sub)
        req_rank = _get_subscription_rank(content_req)
    except ValueError:
        # If either level is unknown, deny access
        return False

    return user_rank >= req_rank


# ----------------------------------------------------------------------
# Main function
# ----------------------------------------------------------------------
def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Return the title of the requested content if the user has permission,
    otherwise return 'Access Denied'.

    Parameters
    ----------
    usr_id : int
        Identifier of the user attempting access.
    contid : int
        Identifier of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.
    """
    # Basic input validation
    if not isinstance(usr_id, int) or not isinstance(contid, int):
        return "Access Denied"

    user = USERS.get(usr_id)
    content = CONTENT.get(contid)

    if user is None or content is None:
        return "Access Denied"

    role = user.get("role", "").lower()
    user_sub = user.get("subscription", "").lower()
    required_sub = content.get("required_subscription", "").lower()

    # Administrators have full access
    if role == "admin":
        return content.get("title", "Access Denied")

    # Regular users: check subscription hierarchy
    if _has_access(user_sub, required_sub):
        return content.get("title", "Access Denied")

    # If the content requires admin but user is not admin
    if required_sub == "admin":
        return "Access Denied"

    # Default denial
    return "Access Denied"


# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin
        (2, 102),  # free user accessing basic content
        (3, 103),  # basic user accessing premium content
        (4, 104),  # premium user accessing admin-only doc
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")