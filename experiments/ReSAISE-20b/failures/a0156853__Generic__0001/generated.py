#!/usr/bin/env python3
"""
Content access authorization module.

The `authorize_access` function checks whether a user identified by `uid`
is allowed to view the content with id `cid`.  Admin users have full
access, while regular users can only view content that matches or is
below their subscription level.
"""

from typing import Dict

# ----------------------------------------------------------------------
# Sample data – in a real system these would come from a database.
# ----------------------------------------------------------------------
USERS: Dict[int, Dict[str, str]] = {
    # user_id : {role: 'admin' | 'user', subscription_level: str}
    1: {"role": "admin", "subscription_level": "gold"},
    2: {"role": "user", "subscription_level": "silver"},
    3: {"role": "user", "subscription_level": "bronze"},
}

CONTENT: Dict[int, Dict[str, str]] = {
    # content_id : {title: str, required_level: str}
    101: {"title": "Premium Article", "required_level": "gold"},
    102: {"title": "Standard Video", "required_level": "silver"},
    103: {"title": "Basic Tutorial", "required_level": "bronze"},
}

# ----------------------------------------------------------------------
# Subscription level hierarchy
# ----------------------------------------------------------------------
LEVEL_ORDER = ["bronze", "silver", "gold"]


def _level_index(level: str) -> int:
    """Return the index of a subscription level; lower is weaker."""
    try:
        return LEVEL_ORDER.index(level)
    except ValueError:
        # Unknown level – treat as the lowest privilege
        return -1


def authorize_access(uid: int, cid: int) -> str:
    """
    Determine if a user can access a piece of content.

    Parameters
    ----------
    uid : int
        The ID of the user attempting access.
    cid : int
        The ID of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted, otherwise 'Access Denied'.

    Raises
    ------
    KeyError
        If the user ID or content ID does not exist.
    """
    # Validate existence of user and content
    if uid not in USERS:
        raise KeyError(f"User ID {uid} does not exist.")
    if cid not in CONTENT:
        raise KeyError(f"Content ID {cid} does not exist.")

    user = USERS[uid]
    content = CONTENT[cid]

    # Admins always have access
    if user.get("role") == "admin":
        return content["title"]

    # Regular users – compare subscription levels
    user_level = _level_index(user.get("subscription_level", ""))
    required_level = _level_index(content.get("required_level", ""))

    if user_level >= required_level:
        return content["title"]

    # If none of the above, deny access
    return "Access Denied"


# ----------------------------------------------------------------------
# Example usage (remove or comment out in production)
# ----------------------------------------------------------------------
if __name__ == "__main__":
    test_cases = [
        (1, 101),  # admin
        (2, 101),  # silver user trying gold content
        (3, 103),  # bronze user accessing bronze content
    ]

    for uid, cid in test_cases:
        try:
            result = authorize_access(uid, cid)
            print(f"User {uid} accessing content {cid}: {result}")
        except KeyError as exc:
            print(f"User {uid} accessing content {cid}: Error – {exc}")