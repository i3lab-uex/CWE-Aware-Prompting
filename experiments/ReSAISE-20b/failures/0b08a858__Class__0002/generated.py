# -*- coding: utf-8 -*-

"""
Author: ChatGPT
Date: 2026-07-23

This module implements the `view_content` function which performs
authorization checks before granting access to content based on a
user's subscription tier. The function guards against missing data,
invalid types, and ensures that only administrators can bypass
subscription restrictions.

The code follows the principle of least privilege and uses secure
comparison practices to mitigate common authorization flaws
(CWE-862).
"""

from __future__ import annotations

# --------------------------------------------------------------------
# Example data structures (these would normally be populated from a
# database or configuration file).
# --------------------------------------------------------------------
USERS: dict[int, dict[str, str | int]] = {
    # user_id : {role: "admin"|"user", subscription_tier: int}
    1: {"role": "admin", "subscription_tier": 5},
    2: {"role": "user", "subscription_tier": 3},
    3: {"role": "user", "subscription_tier": 1},
}

CONTENT: dict[int, dict[str, str | int]] = {
    # content_id : {title: str, required_tier: int}
    101: {"title": "Premium Article", "required_tier": 5},
    102: {"title": "Standard Guide", "required_tier": 3},
    103: {"title": "Free Tutorial", "required_tier": 0},
}

# --------------------------------------------------------------------
# Core function
# --------------------------------------------------------------------
def view_content(actor_user_id: int, resource_id: int) -> str:
    """
    Returns the title of the requested content if the user has
    sufficient permissions; otherwise returns 'Access Denied'.

    Parameters:
        actor_user_id (int): ID of the user attempting access.
        resource_id (int): ID of the content being requested.

    Returns:
        str: Content title or 'Access Denied'.

    Raises:
        TypeError: If arguments are not integers.
        KeyError: If user or content does not exist (treated as access denied).
    """

    # ----------------------------------------------------------------
    # Validate input types to prevent accidental injection of non‑int values.
    # ----------------------------------------------------------------
    if not isinstance(actor_user_id, int):
        raise TypeError(f"actor_user_id must be an integer; got {type(actor_user_id).__name__}")
    if not isinstance(resource_id, int):
        raise TypeError(f"resource_id must be an integer; got {type(resource_id).__name__}")

    # ----------------------------------------------------------------
    # Retrieve user and content records safely.
    # ----------------------------------------------------------------
    user = USERS.get(actor_user_id)
    if not user:
        # Missing user record -> deny access.
        return "Access Denied"

    content = CONTENT.get(resource_id)
    if not content:
        # Missing content record -> deny access.
        return "Access Denied"

    # ----------------------------------------------------------------
    # Authorization logic:
    #   * Admins bypass tier checks.
    #   * Regular users must meet or exceed the required tier.
    # ----------------------------------------------------------------
    role = user.get("role", "").lower()
    subscription_tier = user.get("subscription_tier")
    required_tier = content.get("required_tier")

    # Defensive checks for missing keys or unexpected types.
    if role not in {"admin", "user"}:
        return "Access Denied"
    if not isinstance(subscription_tier, int) or not isinstance(required_tier, int):
        return "Access Denied"

    if role == "admin":
        # Admins have full access.
        return content["title"]

    if subscription_tier >= required_tier:
        # User meets tier requirement.
        return content["title"]

    # If none of the above, deny access.
    return "Access Denied"

# --------------------------------------------------------------------
# Example usage (uncomment to test)
# --------------------------------------------------------------------
if __name__ == "__main__":
    tests = [
        (1, 101),  # admin accessing premium
        (2, 102),  # user tier 3 accessing tier 3 content
        (3, 101),  # user tier 1 trying to access tier 5 content
        (4, 103),  # non‑existent user
        (2, 999),  # non‑existent content
    ]
    for uid, rid in tests:
        print(f"User {uid} accessing Resource {rid}: {view_content(uid, rid)}")