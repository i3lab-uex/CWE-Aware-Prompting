# -*- coding: utf-8 -*-
"""
Utility module for content access control.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data – in a real application these would come from a database or
# external service.  The structure is intentionally simple to keep the
# example focused on access logic.
# --------------------------------------------------------------------------- #

USERS = {
    1: {"user_id": 1, "role": "admin", "subscription_level": None},
    2: {"user_id": 2, "role": "user", "subscription_level": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_level": "premium"},
    # ... additional users
}

CONTENT = {
    101: {"title": "Public Article",      "required_level": None},
    102: {"title": "Basic Video",         "required_level": "basic"},
    103: {"title": "Premium Webinar",     "required_level": "premium"},
    # ... additional content
}

# --------------------------------------------------------------------------- #
# Access control implementation
# --------------------------------------------------------------------------- #

def authorize_access(uid: int, cid: int) -> str:
    """
    Determine whether a user may access a particular piece of content.

    Parameters
    ----------
    uid : int
        The identifier of the user attempting access.
    cid : int
        The identifier of the content being requested.

    Returns
    -------
    str
        The title of the requested content if access is granted,
        otherwise ``'Access Denied'``.

    Raises
    ------
    ValueError
        If either the user or content identifier does not exist.
    TypeError
        If ``uid`` or ``cid`` is not an integer.

    Notes
    -----
    - Admin users (role == 'admin') have unconditional access.
    - Regular users may only view content whose required subscription level
      is less than or equal to their own.
    - Content with ``required_level`` set to ``None`` is considered public.
    """
    # --------------------------------------------------------------------- #
    # Basic input validation – protects against accidental misuse and
    # ensures predictable behaviour.
    # --------------------------------------------------------------------- #
    if not isinstance(uid, int):
        raise TypeError(f"uid must be an integer, got {type(uid).__name__}")
    if not isinstance(cid, int):
        raise TypeError(f"cid must be an integer, got {type(cid).__name__}")

    # --------------------------------------------------------------------- #
    # Retrieve user and content data.
    # --------------------------------------------------------------------- #
    user = USERS.get(uid)
    if user is None:
        raise ValueError(f"User with id {uid} does not exist.")

    content = CONTENT.get(cid)
    if content is None:
        raise ValueError(f"Content with id {cid} does not exist.")

    # --------------------------------------------------------------------- #
    # Admins bypass all checks.
    # --------------------------------------------------------------------- #
    if user.get("role") == "admin":
        return content["title"]

    # --------------------------------------------------------------------- #
    # For regular users, compare subscription levels.
    # The hierarchy is defined by the order in SUBSCRIPTION_HIERARCHY.
    # --------------------------------------------------------------------- #
    subscription_hierarchy = ["free", "basic", "premium"]

    user_level = user.get("subscription_level")
    required_level = content.get("required_level")

    # Public content is accessible to everyone.
    if required_level is None:
        return content["title"]

    # If user has no subscription level, treat them as 'free'.
    if user_level is None:
        user_level = "free"

    # Verify that the user's level is sufficient.
    try:
        user_index = subscription_hierarchy.index(user_level)
        required_index = subscription_hierarchy.index(required_level)
    except ValueError as exc:
        # Unexpected level – safest to deny access.
        return "Access Denied"

    if user_index >= required_index:
        return content["title"]

    # If none of the above conditions matched, deny access.
    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (commented out – remove comments to test manually)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # print(authorize_access(1, 101))  # Admin access
    # print(authorize_access(2, 102))  # Basic user accessing basic content
    # print(authorize_access(2, 103))  # Basic user denied premium content
    pass