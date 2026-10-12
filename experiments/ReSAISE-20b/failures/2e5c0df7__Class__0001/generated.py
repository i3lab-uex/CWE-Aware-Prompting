# -*- coding: utf-8 -*-

"""
Author: OpenAI ChatGPT
Date: 2026-07-23

This module implements a simple access control function `get_content` that
checks whether a user is authorized to view a specific piece of content.
"""

from typing import Dict, Any

# --------------------------------------------------------------------------- #
# Data structures – in a real system these would come from a database
# --------------------------------------------------------------------------- #

USERS: Dict[int, Dict[str, Any]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": None},
    2: {"user_id": 2, "role": "user", "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user", "subscription_tier": "premium"},
    # ... add more users as needed
}

# Subscription tiers are represented by an integer rank; higher numbers mean higher access.
TIER_RANKS: Dict[str, int] = {
    "basic": 1,
    "premium": 2,
    "vip": 3
}

CONTENT: Dict[int, Dict[str, Any]] = {
    101: {"content_id": 101, "title": "Public Article", "required_tier": "basic"},
    102: {"content_id": 102, "title": "Premium Video", "required_tier": "premium"},
    103: {"content_id": 103, "title": "VIP Webinar", "required_tier": "vip"},
    # ... add more content items as needed
}

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def _get_user(user_id: int) -> Dict[str, Any] | None:
    """Retrieve user data from the USERS dictionary."""
    return USERS.get(user_id)

def _get_content(item_id: int) -> Dict[str, Any] | None:
    """Retrieve content data from the CONTENT dictionary."""
    return CONTENT.get(item_id)

def _has_access(user: Dict[str, Any], content: Dict[str, Any]) -> bool:
    """
    Determine if the user has sufficient subscription tier to access the content.
    Administrators bypass all checks.
    """
    if user["role"] == "admin":
        return True

    # Non-admin users must have a tier that meets or exceeds the required tier.
    user_tier = user.get("subscription_tier")
    if not user_tier:
        return False  # No tier assigned to a non‑admin

    required_tier = content.get("required_tier")
    if not required_tier:
        return False  # Content has no defined tier; deny by default

    user_rank = TIER_RANKS.get(user_tier, 0)
    required_rank = TIER_RANKS.get(required_tier, 0)

    return user_rank >= required_rank

# --------------------------------------------------------------------------- #
# Main function
# --------------------------------------------------------------------------- #

def get_content(active_user_id: int, item_id: int) -> str:
    """
    Return the title of the requested content if the user has permission.
    Otherwise, return 'Access Denied'.

    Parameters
    ----------
    active_user_id : int
        The ID of the user attempting to access content.
    item_id : int
        The ID of the content being requested.

    Returns
    -------
    str
        Content title or 'Access Denied'.

    Raises
    ------
    ValueError
        If the user or content does not exist.
    """
    # Fetch user and content records
    user = _get_user(active_user_id)
    if not user:
        raise ValueError(f"User with ID {active_user_id} does not exist.")

    content = _get_content(item_id)
    if not content:
        raise ValueError(f"Content with ID {item_id} does not exist.")

    # Authorization check
    if _has_access(user, content):
        return content["title"]

    return "Access Denied"

# --------------------------------------------------------------------------- #
# Example usage (uncomment to test)
# --------------------------------------------------------------------------- #

if __name__ == "__main__":
    # Test cases
    for uid in [1, 2, 3]:
        for cid in [101, 102, 103]:
            try:
                result = get_content(uid, cid)
                print(f"User {uid} accessing item {cid}: {result}")
            except ValueError as e:
                print(e)