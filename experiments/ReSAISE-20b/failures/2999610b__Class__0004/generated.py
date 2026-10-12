#!/usr/bin/env python3
"""
Secure content retrieval module.

The module enforces authorization based on user role and subscription level.
Administrators are granted full access. Regular users may only access content
whose required subscription level is less than or equal to their own.
"""

from typing import Dict, List

# --------------------------------------------------------------------------- #
# Sample data – in a real system these would come from a database or an
# external service.  The values are kept intentionally small for clarity.
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, str]] = {
    1: {"role": "admin", "subscription": "gold"},
    2: {"role": "user", "subscription": "silver"},
    3: {"role": "user", "subscription": "bronze"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    101: {"title": "Advanced AI", "required_level": "gold"},
    102: {"title": "Machine Learning Basics", "required_level": "silver"},
    103: {"title": "Intro to Programming", "required_level": "bronze"},
}

# The hierarchy defines the order from lowest to highest.
SUBSCRIPTION_HIERARCHY: List[str] = ["bronze", "silver", "gold"]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_subscription_rank(level: str) -> int:
    """
    Convert a subscription level to its rank in the hierarchy.
    Returns -1 if the level is unknown, which indicates a security error
    and will deny access.
    """
    try:
        return SUBSCRIPTION_HIERARCHY.index(level)
    except ValueError:
        # Unknown subscription level – treat as the lowest privilege
        return -1


def _has_access(user_level: str, content_level: str) -> bool:
    """
    Determine whether a user with `user_level` can access content requiring
    `content_level`.  The comparison is inclusive: a higher or equal level grants access.
    """
    user_rank = _get_subscription_rank(user_level)
    content_rank = _get_subscription_rank(content_level)

    # If either rank is -1 (unknown level), deny access
    if user_rank == -1 or content_rank == -1:
        return False

    return user_rank >= content_rank


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #

def retrieve_content(usr_id: int, contid: int) -> str:
    """
    Retrieve the title of content identified by `contid` for user `usr_id`.

    Parameters
    ----------
    usr_id : int
        Identifier of the requesting user.
    contid : int
        Identifier of the content to retrieve.

    Returns
    -------
    str
        The title of the requested content if access is granted,
        otherwise "Access Denied".

    Raises
    ------
    KeyError
        If the user or content identifier does not exist.
    """
    # Fetch user and content records securely
    try:
        user = USERS[usr_id]
    except KeyError as exc:
        raise KeyError(f"User ID {usr_id} not found.") from exc

    try:
        content = CONTENT[contid]
    except KeyError as exc:
        raise KeyError(f"Content ID {contid} not found.") from exc

    # Admin bypass – full access
    if user.get("role") == "admin":
        return content["title"]

    # Regular user – check subscription level
    if _has_access(user.get("subscription", ""), content.get("required_level", "")):
        return content["title"]

    # Default: deny access
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (for testing only; remove or guard with __name__ == "__main__")
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin accessing gold content
        (2, 101),  # silver user trying to access gold content
        (3, 103),  # bronze user accessing bronze content
        (3, 102),  # bronze user trying to access silver content
    ]

    for uid, cid in test_cases:
        print(f"User {uid} accessing content {cid}: {retrieve_content(uid, cid)}")