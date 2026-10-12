# -*- coding: utf-8 -*-
"""
A simple access‑control helper that checks whether a user is allowed to
retrieve a piece of content based on their subscription level.

The module intentionally performs all necessary validation and authorization
checks to mitigate CWE‑862 (Missing Authorization).
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# Sample data structures
# --------------------------------------------------------------------------- #

USERS = {
    1: {"role": "admin", "subscription_tier": "premium"},
    2: {"role": "user",  "subscription_tier": "basic"},
    3: {"role": "user",  "subscription_tier": "premium"},
}

CONTENT = {
    101: {"title": "Intro to Python",   "required_tier": "basic"},
    102: {"title": "Advanced AI",      "required_tier": "premium"},
    103: {"title": "Admin Guide",      "required_tier": "admin_only"},
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _validate_int(value: int, name: str) -> None:
    """Ensure that a value is an integer."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer, got {type(value).__name__}")

def _get_user(user_id: int) -> dict:
    """Retrieve a user record, raising an informative error if missing."""
    try:
        return USERS[user_id]
    except KeyError as exc:
        raise ValueError(f"User with id {user_id} does not exist") from exc

def _get_content(content_id: int) -> dict:
    """Retrieve a content record, raising an informative error if missing."""
    try:
        return CONTENT[content_id]
    except KeyError as exc:
        raise ValueError(f"Content with id {content_id} does not exist") from exc

# --------------------------------------------------------------------------- #
# Core functionality
# --------------------------------------------------------------------------- #

def retrieve_content(user_id: int, content_id: int) -> str:
    """
    Return the title of a content item if the user is authorized to view it.
    
    Parameters
    ----------
    user_id : int
        The identifier of the user attempting to access content.
    content_id : int
        The identifier of the requested content.

    Returns
    -------
    str
        The title of the content if access is granted; otherwise,
        'Access Denied'.

    Raises
    ------
    TypeError
        If either argument is not an integer.
    ValueError
        If the user or content does not exist in the data stores.
    """
    # Input validation
    _validate_int(user_id, "user_id")
    _validate_int(content_id, "content_id")

    # Fetch records
    user = _get_user(user_id)
    content = _get_content(content_id)

    # Authorization logic
    role = user.get("role")
    tier = user.get("subscription_tier")

    # Admins bypass all checks
    if role == "admin":
        return content["title"]

    # Content that is restricted to admins only
    if content.get("required_tier") == "admin_only":
        return "Access Denied"

    # Standard tier comparison
    required = content.get("required_tier")
    allowed_tiers = {"basic": 1, "premium": 2}
    
    # Ensure tiers are known
    if tier not in allowed_tiers or required not in allowed_tiers:
        return "Access Denied"

    if allowed_tiers[tier] >= allowed_tiers[required]:
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (remove or comment out in production)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Expected: "Intro to Python"
    print(retrieve_content(2, 101))
    
    # Expected: "Access Denied" (basic user cannot access premium)
    print(retrieve_content(2, 102))
    
    # Expected: "Advanced AI" (admin can access anything)
    print(retrieve_content(1, 102))