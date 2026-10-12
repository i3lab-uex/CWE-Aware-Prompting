# -*- coding: utf-8 -*-
"""
Author: ChatGPT
Date: 2026-07-23

This module provides a single function `view_content` that enforces
access control based on user role and subscription tier.  The function
returns the content title if access is granted or 'Access Denied'
otherwise.

The implementation follows best practices to mitigate CWE-284
(Improper Access Control) by:
1. Using explicit role checks.
2. Comparing subscription levels in a deterministic order.
3. Avoiding the use of `eval` or other unsafe dynamic code.
"""

from typing import Dict

# Example data structures (should be replaced with real persistence in production)
USERS: Dict[int, Dict[str, str]] = {
    1: {"user_id": 1, "role": "admin", "subscription_tier": "premium"},
    2: {"user_id": 2, "role": "user",  "subscription_tier": "basic"},
    3: {"user_id": 3, "role": "user",  "subscription_tier": "premium"},
}

# Content required subscription tier
CONTENT: Dict[int, Dict[str, str]] = {
    101: {"content_id": 101, "title": "Basic Guide",   "required_tier": "basic"},
    102: {"content_id": 102, "title": "Premium Insights", "required_tier": "premium"},
    103: {"content_id": 103, "title": "Admin Manual",  "required_tier": "admin"},
}

# Define a deterministic ordering of subscription tiers
TIER_ORDER = {"basic": 1, "premium": 2, "admin": 3}


def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Returns the title of the requested content if the user has sufficient
    privileges. Otherwise returns 'Access Denied'.

    Parameters:
        actor_user_id (int): ID of the user attempting access.
        resource_id (int): ID of the content being requested.

    Returns:
        str: Content title or 'Access Denied'.
    """
    # Retrieve user and resource data safely
    user = USERS.get(actor_user_id)
    content = CONTENT.get(resource_id)

    if not user or not content:
        # If either the user or content is missing, deny access
        return "Access Denied"

    # Administrators can access any content
    if user.get("role") == "admin":
        return content.get("title", "Access Denied")

    # For regular users, compare subscription tiers
    user_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # If any tier information is missing, deny access
    if user_tier not in TIER_ORDER or required_tier not in TIER_ORDER:
        return "Access Denied"

    # Grant access if user's tier level is >= required tier
    if TIER_ORDER[user_tier] >= TIER_ORDER[required_tier]:
        return content.get("title", "Access Denied")

    # All other cases are denied
    return "Access Denied"